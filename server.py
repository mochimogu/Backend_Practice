from flask import Flask, render_template, jsonify, request, json, redirect, url_for
import database

app = Flask(__name__, static_folder='static')


database.setup()

@app.route('/')
def start():
    return render_template("app.html"), 200

#THIS WILL GENERATE THE BLOG AS A NEW OR STILL EDITING
@app.route('/edit')
def edit():
    
    return render_template("editBlog.html", existed=False) , 200

@app.route('/edit/<id>', methods=["GET"])
def editById(id):
        
    return render_template("editBlog.html", existed=True) , 200

# THIS WILL GENERATE THE BLOG AND DISPLAY IT AS READ ONLY
@app.route('/read')
def read():
    return render_template("readBlog.html"), 200


@app.route('/read/<title>', methods=["GET", "POST"])
def readBlog():
    
    
    
    return render_template("readBlog.html"), 200

#THIS WILL GENERATE A BUNCH OF BLOGS FOR USER TO CLICK TO READ
@app.route('/browse', methods=["GET"])
def browse():
    
    blogs = database.selectBlogsByPublished()
    
    return render_template("browse.html", data=blogs), 200

@app.route('/myBlogs')
def userBlogs():
    
    blogs = database.selectAllBlog()
    
    
    return render_template("userBlogs.html", data=blogs), 200
# ====================================================================
@app.route('/saveBlog', methods=["POST", "GET"])
def saveBlog():
    
    if(request.is_json):
        data = request.get_json()
        print(data)
        
        database.saveBlog(data)
        # print(database.selectAllBlog())
    
    return render_template("editBlog.html")
    
@app.route('/api/edit/<id>', methods=["POST", "GET"])
def apiEdit(id):
    
    print(id)
    blog = database.selectBlogsByID(id)
    
    sending = {
        'id' : blog[0],
        'title' : blog[1],
        'category' : blog[2],
        'tags' : blog[3],
        'delta' : json.loads(blog[4])
    }
    
    return jsonify(sending)

@app.route('/api/update/<id>', methods=["POST", "GET"])
def updateBlog(id):
    
    if(request.is_json):
        data = request.get_json()
        print(data)
            
        database.updateBlog(data)
    
    return render_template("editBlog.html", existed=True) , 200
    
@app.route('/api/published/<id>', methods=["POST", "GET"])
def pushlishBlog(id):
    if(request.is_json):
        data = request.get_json()
        print(data)
    
        database.publishBlog(data)
    
    return render_template("editBlog.html", existed=True) , 200


if __name__ == "__main__":
    app.run(debug=True)