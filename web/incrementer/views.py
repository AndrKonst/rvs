from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Num

import psycopg2 as sql
import os, json

@csrf_exempt
def curl(request):
    # http method check
    if request.method == 'POST':
        in_data = json.loads(request.body)

        # number check
        for i in in_data.values():
            if type(i) != int:
                ans = {'msg': 'Wrong type of input data'}
                return HttpResponse(JsonResponse(ans))
            if i < 0:
                ans = {'msg': 'input number must be positive'}
                return HttpResponse(JsonResponse(ans))

        # db connection
        try:
            conn = sql.connect(dbname=os.environ.get('RVS_DB_NAME'),
                               user=os.environ.get('RVS_DB_USER'),
                               password=os.environ.get('RVS_DB_PASS'),
                               host=os.environ.get('RVS_DB_HOST'),
                               port=os.environ.get('RVS_DB_PORT'))
        except sql.OperationalError as err:
            ans = {'msg': 'Connection db error: {}'.format(err)}
            return HttpResponse(JsonResponse(ans))
        cur = conn.cursor()

        # creation tables
        cur.execute('CREATE TABLE IF NOT EXISTS nums (num INTEGER PRIMARY KEY)')
        conn.commit()

        cur.execute('CREATE TABLE IF NOT EXISTS incrementer_conflicts \
                    (id SERIAL PRIMARY KEY,\
                     conflict_type INTEGER NOT NULL,\
                     number INTEGER REFERENCES nums (num) ON DELETE CASCADE,\
                     date_time TIMESTAMP )')
        conn.commit()

        # check for conflicts
        for num in in_data.values():
            cur.execute('SELECT num, num-1 FROM nums WHERE num=%s', (num,))
            db_nums = cur.fetchone()
            if not db_nums:
                cur.execute('INSERT INTO nums VALUES (%s)', (num,))
                conn.commit()
                cur.close()
                conn.close()
                ans = {'msg': 'Number {} processed'.format(num)}
                return HttpResponse(JsonResponse(ans))
            elif num == db_nums[0]:
                cur.execute('INSERT INTO incrementer_conflicts (conflict_type, number, date_time) \
                             VALUES (1, %s, now())', (num,))
                conn.commit()
                cur.close()
                conn.close()
                ans = {'msg': 'Conflict 1. Number {} has already been processed'.format(num,)}
                return HttpResponse(JsonResponse(ans))
            elif num == db_nums[1]:
                cur.execute('INSERT INTO incrementer_conflicts (conflict_type, number, date_time) \
                             VALUES (2, %s, now())', (num,))
                conn.commit()
                cur.close()
                conn.close()
                ans = {'msg': 'Conflict 2. Number {} is 1 less then the previously processed number'.format(num,)}
                return HttpResponse(JsonResponse(ans))

    # actions if method not post
    else:
        ans = {'msg': 'HTTP method not POST'}
        return HttpResponse(JsonResponse(ans))


def clear_db(request):
    for t in Num.objects.all():
        t.delete()
    ans = {'msg': 'Db cleared'}
    return HttpResponse(JsonResponse(ans))
