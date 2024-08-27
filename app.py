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
    title = request.args.get('title').strip()
    authors = request.args.get('authors').strip()
    abstract = request.args.get('abstract').strip()
    topics = request.args.get('topics').strip()
    result = request.args.get('result').strip()
    if title == '' or authors == '' or abstract == '' or topics == '' or result == '':
        return render_template("add_papers.html", success='Please fill all fields.')
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `paper`(`title`, `abstract`, `result`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (title, abstract, result))

            sql = "SELECT id FROM `paper` WHERE `title` = %s"
            cursor.execute(sql, title)
            result = cursor.fetchone()
            paper_id = result["id"]

            authors = authors.split(',')
            for x in authors:
                author = x.split()
                name = author[0].strip()
                surname = author[1].strip()

                sql = "SELECT id FROM `author` WHERE `name` = %s AND `surname` = %s"
                cursor.execute(sql, (name, surname))
                result = cursor.fetchone()
                author_id = result["id"]

                sql = "INSERT INTO `author_paper`(`author_id`, `paper_id`) VALUES (%s, %s)"
                cursor.execute(sql, (author_id, paper_id))

            topics = topics.split(',')
            for topic in topics:
                topic = topic.strip()

                sql = "SELECT id FROM `topic` WHERE `name` = %s"
                cursor.execute(sql, topic)
                result = cursor.fetchone()
                topic_id = result["id"]

                sql = "INSERT INTO `topic_paper`(`topic_id`, `paper_id`) VALUES (%s, %s)"
                cursor.execute(sql, (topic_id, paper_id))

            return render_template("add_papers.html", success='Successful')
    except Exception as e:
        return render_template("add_papers.html", success='Can\'t add Paper: ' + str(e))


@app.route('/updatePapers')
def update_papers_page():
    return render_template("update_papers.html", success='')

@app.route('/updatePaperReq', methods=['GET'])
def update_paper():
    old_title = request.args.get('old_title').strip()
    title = request.args.get('title').strip()
    authors = request.args.get('authors').strip()
    abstract = request.args.get('abstract').strip()
    topics = request.args.get('topics').strip()
    result = request.args.get('result').strip()

    if old_title == '' or title == '' or authors == '' or abstract == '' or topics == '' or result == '':
        return render_template("add_papers.html", success='Please fill all fields.')
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE `paper` SET `title`=%s,`abstract`=%s,`result`=%s WHERE `title`=%s"
            cursor.execute(sql, (title, abstract, result, old_title))

            sql = "SELECT id FROM `paper` WHERE `title` = %s"
            cursor.execute(sql, title)
            result = cursor.fetchone()
            paper_id = result["id"]

            sql = "DELETE FROM `author_paper` WHERE `paper_id`=%s"
            cursor.execute(sql, paper_id)
            sql = "DELETE FROM `topic_paper` WHERE `paper_id`=%s"
            cursor.execute(sql, paper_id)

            authors = authors.split(',')
            for x in authors:
                author = x.split()
                name = author[0].strip()
                surname = author[1].strip()

                sql = "SELECT id FROM `author` WHERE `name` = %s AND `surname` = %s"
                cursor.execute(sql, (name, surname))
                result = cursor.fetchone()
                author_id = result["id"]

                sql = "INSERT INTO `author_paper`(`author_id`, `paper_id`) VALUES (%s, %s)"
                cursor.execute(sql, (author_id, paper_id))

            topics = topics.split(',')
            for topic in topics:
                topic = topic.strip()

                sql = "SELECT id FROM `topic` WHERE `name` = %s"
                cursor.execute(sql, topic)
                result = cursor.fetchone()
                topic_id = result["id"]

                sql = "INSERT INTO `topic_paper`(`topic_id`, `paper_id`) VALUES (%s, %s)"
                cursor.execute(sql, (topic_id, paper_id))

            return render_template("update_papers.html", success='Successful')
    except Exception as e:
        return render_template("update_papers.html", success='Can\'t update Paper: ' + str(e))


@app.route('/deletePapers')
def delete_papers_page():
    return render_template("delete_papers.html", success='')

@app.route('/deletePaperReq', methods=['GET'])
def delete_paper():
    title = request.args.get('title').strip()
    if title == '':
        return render_template("delete_papers.html", success='Title cannot be empty')
    try:
        with connection.cursor() as cursor:
            sql = "SELECT id FROM `paper` WHERE `title` = %s"
            cursor.execute(sql, title)
            result = cursor.fetchone()
            paper_id = result["id"]

            sql = "DELETE FROM `author_paper` WHERE `paper_id`=%s"
            cursor.execute(sql, paper_id)

            sql = "DELETE FROM `topic_paper` WHERE `paper_id`=%s"
            cursor.execute(sql, paper_id)

            sql = "DELETE FROM `paper` WHERE `title`=%s"
            cursor.execute(sql, title)

            return render_template("delete_papers.html", success='Successful')
    except Exception as e:
        return render_template("delete_papers.html", success='Can\'t delete paper: ' + str(e))


@app.route('/viewPapers')
def view_papers_page():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT DISTINCT paper.id, title, abstract, result, " \
                  "GROUP_CONCAT(DISTINCT \' \', `author`.name, \' \', `author`.surname) as authors, " \
                  "GROUP_CONCAT(DISTINCT `topic`.name) as topics " \
                  "FROM `paper` " \
                  "JOIN `author_paper` ON `paper`.id = `author_paper`.paper_id " \
                  "JOIN `topic_paper` ON `paper`.id = `topic_paper`.paper_id " \
                  "JOIN `author` ON author_id = `author`.id " \
                  "JOIN `topic` ON `topic`.id = topic_id " \
                  "GROUP BY paper.id"
            cols = ['id', 'title', 'abstract', 'result', 'authors', 'topics']
            cursor.execute(sql)
            result = cursor.fetchall()
            return render_template("view_papers.html", items=result, cols=cols, success='')
    except Exception as e:
        return render_template("view_papers.html", items=[], cols=[], success='Can\'t view Papers: ' + str(e))

if __name__ == '__main__':
    app.run()