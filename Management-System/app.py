from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='1234',
                             db='task_list',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)


@app.route('/')
def login():
    return render_template("index.html")


@app.route('/homeAdmin')
def home_admin():
    return render_template("home_admin.html")


@app.route('/homeUser')
def home_user():
    return render_template("home_user.html")


@app.route('/addPapers')
def add_papers_page():
    return render_template("add_papers.html", success='')

@app.route('/addPaperReq', methods=['GET'])
def add_paper():
    id = request.args.get('id').strip()
    name = request.args.get('name').strip()
    age = request.args.get('age').strip()
    if id == '' or name == '' or age == '':
        return render_template("add_papers.html", success='Please fill all fields.')
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO task_list.user (id, name, age) VALUES (%s,%s,%s);"
            cursor.execute(sql, (int(id), name, int(age)))
            connection.commit()

            return render_template("add_papers.html", success='Successful')
    except Exception as e:
        return render_template("add_papers.html", success='Can\'t add Paper: ' + str(e))


@app.route('/updatePapers')
def update_papers_page():
    return render_template("update_papers.html", success='')

@app.route('/updatePaperReq', methods=['GET'])
def update_paper():
    old_id = request.args.get('old_id').strip()
    id = request.args.get('id').strip()
    name = request.args.get('name').strip()
    age = request.args.get('age').strip()

    if old_id == '' or id == '' or name == '' or age == '':
        return render_template("add_papers.html", success='Please fill all fields.')
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE `user` SET `id`=%s,`name`=%s,`age`=%s WHERE `id`=%s"
            cursor.execute(sql, (id, name, age, old_id))
            connection.commit()

            return render_template("update_papers.html", success='Successful')
    except Exception as e:
        return render_template("update_papers.html", success='Can\'t update Paper: ' + str(e))


@app.route('/deletePapers')
def delete_papers_page():
    return render_template("delete_papers.html", success='')

@app.route('/deletePaperReq', methods=['GET'])
def delete_paper():
    name = request.args.get('name').strip()
    if name == '':
        return render_template("delete_papers.html", success='Name cannot be empty')
    try:
        with connection.cursor() as cursor:

            sql = "DELETE FROM user WHERE name =%s"
            cursor.execute(sql, name)
            connection.commit()

            return render_template("delete_papers.html", success='Successful')
    except Exception as e:
        return render_template("delete_papers.html", success='Can\'t delete paper: ' + str(e))


@app.route('/viewPapers')
def view_papers_page():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM task_list.user;"
            cols = ['id', 'name', 'age']
            cursor.execute(sql)
            result = cursor.fetchall()
            return render_template("view_papers.html", items=result, cols=cols, success='')
    except Exception as e:
        return render_template("view_papers.html", items=[], cols=[], success='Can\'t view Papers: ' + str(e))

if __name__ == '__main__':
    app.run()