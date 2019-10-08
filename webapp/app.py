from flask import Flask
import docker

client = docker.from_env()
app = Flask(__name__)

@app.route("/images/list")
def find_image():
    images = client.images.list()
    res = {each.id:each.labels for each in images}
    return res

@app.route("/images/pull/<image>")
@app.route("/images/pull/<image>/<tag>")
def pull_image(image,tag=None):
    try:
        res = client.images.pull(image, tag)
        if isinstance(client.images, res):
            res = res.id
    except docker.errors.APIError as e:
        res = {"failed" : str(e)}
    finally:
        return res

@app.route("/images/prune")
def prune():
    res = client.images.prune()
    return res

@app.route("/container/run/<image>")
@app.route("/container/run/<image>/<command>")
def run(image, command=None):
    resp = client.containers.run(image,command, detach=True)
    print(resp)
    return 'okay'

@app.route("/container/get/all")
def get_all_container():
    try:
        res = client.containers.list(sparse=bool)
        res.reload()
        print(res)
    except docker.errors.APIError as e:
        resp =  {"failed" : str(e)}
    
    finally:
        return "<h4>hi</h4>"
        

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)