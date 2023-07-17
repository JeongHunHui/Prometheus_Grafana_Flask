from flask import request, jsonify
import pymysql
import time
from app import app
from app.db_manager import db_manager

@app.route('/hotels', methods=['GET'])
def find_hotels():
    start_time = time.time()
    connection = db_manager.get_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    people_count = request.args.get('count')
    region_id = request.args.get('region')
    category_id = request.args.get('category')
    cursor_id = request.args.get('cursor')

    if not all(param is not None and param.isdigit() for param in [people_count, region_id, category_id, cursor_id]):
        return "Invalid Parameters", 400

    sql = """
            SELECT h.name       AS hotel_name,
                   MIN(r.price) AS price,
                   rating,
                   address,
                   detail_region_name,
                   category_name
            FROM hotels h
                JOIN rooms r
                    ON h.id = r.hotel_id
                        AND r.max_people_count >= %s
            WHERE h.region_id = %s
                AND h.category_id = %s
                AND h.id > %s
            GROUP BY h.id
            ORDER BY h.id
            LIMIT 20;
        """
    cursor.execute(sql, (people_count, region_id, category_id, cursor_id))

    result = cursor.fetchall()
    status_code = 200 if result else 404

    return jsonify(result), status_code
