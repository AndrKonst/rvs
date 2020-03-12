from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

import psycopg2 as sql
import os, json

@csrf_exempt
def increment(request):
    # http method check
    if request.method == 'POST':
        in_data = json.loads(request.body)

        # number check
        num = None
        # check for 1 number
        if len(in_data) > 1:
            ans = {'msg': 'Entered more then 1 number'}
            return JsonResponse(ans)
        for i in in_data.values():
            if type(i) != int:
                ans = {'msg': 'Wrong type of input data'}
                return JsonResponse(ans)
            if i < 0:
                ans = {'msg': 'input number must be positive'}
                return JsonResponse(ans)
            num = i

        # db connection
        try:
            conn = sql.connect(dbname=os.environ.get('RVS_DB_NAME'),
                               user=os.environ.get('RVS_DB_USER'),
                               password=os.environ.get('RVS_DB_PASS'),
                               host=os.environ.get('RVS_DB_HOST'),
                               port=os.environ.get('RVS_DB_PORT'))
            cur = conn.cursor()

        except sql.OperationalError as err:
            ans = {'msg': 'Connection db error: {}'.format(err)}
            return JsonResponse(ans)

        # creation tables
        cur.execute('CREATE TABLE IF NOT EXISTS nums (num INTEGER PRIMARY KEY)')
        conn.commit()

        cur.execute('CREATE TABLE IF NOT EXISTS incrementer_conflicts \
                    (id SERIAL PRIMARY KEY,\
                     conflict_type INTEGER NOT NULL,\
                     number INTEGER REFERENCES nums (num) ON DELETE CASCADE,\
                     date_time TIMESTAMP )')
        conn.commit()


        #check for conflicts
        if num:
            cur.execute('SELECT num FROM nums WHERE num=%s or num=%s+1', (num, num))
            db_nums = cur.fetchone()
            if not db_nums:
                cur.execute('INSERT INTO nums VALUES (%s)', (num,))
                conn.commit()
                ans = {'msg': 'Number {} processed'.format(num)}
                return JsonResponse(ans)
            elif num == db_nums[0]:
                cur.execute('INSERT INTO incrementer_conflicts (conflict_type, number, date_time) \
                             VALUES (1, %s, now())', (num,))
                conn.commit()
                ans = {'msg': 'Conflict 1. Number {} has already been processed'.format(num,)}
                return JsonResponse(ans)
            elif num + 1 == db_nums[0]:
                cur.execute('INSERT INTO incrementer_conflicts (conflict_type, number, date_time) \
                             VALUES (2, %s, now())', (num + 1,))
                conn.commit()
                ans = {'msg': 'Conflict 2. Number {} is 1 less then the previously processed number'.format(num,)}
                return JsonResponse(ans)
        else:
            ans = {'msg': 'Number not entered'}
            return JsonResponse(ans)


    # actions if method not post
    else:
        ans = {'msg': 'HTTP method not POST'}
        return JsonResponse(ans)

@csrf_exempt
def clear_db(request):
    # db connection
    try:
        conn = sql.connect(dbname=os.environ.get('RVS_DB_NAME'),
                           user=os.environ.get('RVS_DB_USER'),
                           password=os.environ.get('RVS_DB_PASS'),
                           host=os.environ.get('RVS_DB_HOST'),
                           port=os.environ.get('RVS_DB_PORT'))
        cur = conn.cursor()

    except sql.OperationalError as err:
        ans = {'msg': 'Connection db error: {}'.format(err)}
        return JsonResponse(ans)

    # drop table nums to clear db
    cur.execute('DROP TABLE IF EXISTS nums CASCADE')
    cur.execute('DROP TABLE IF EXISTS incrementer_conflicts CASCADE')

    conn.commit()

    ans = {'msg': 'Tables dropped'}
    return JsonResponse(ans)
