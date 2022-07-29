import cv2
from flask import Flask, request, render_template, Response,jsonify,json
app = Flask(__name__)
old_message = ""
message = ""

@app.route('/')
def main():
    slider1_num = 12
    slider2_num = 34
    slider3_num = 56
    return render_template('index.html',slider1_num = slider1_num,slider2_num = slider2_num,slider3_num = slider3_num)

@app.route('/index',methods=['GET'])
def index():
    if request.method == 'GET':
        input_text = request.args['input_text']
        print(input_text)
    return jsonify({'code': 0, 'msg': 'success'})

@app.route('/test',methods=['GET'])
def test():
    if request.method == 'GET':
        test = request.args['test']
        if test == '1':
            print('测试1被点击')
            sen_message('123456789') # 发送日志信息
        if test == '2':
            print('测试2被点击')
    return jsonify({'code': 0, 'msg': 'success'})

# 三个滑块
@app.route('/slider1',methods=['GET'])
def slider1():
    value = request.args['value']
    print('slider1 ' + value)
    return jsonify({'code': 0, 'msg': 'success'})

@app.route('/slider2',methods=['GET'])
def slider2():
    value = request.args['value']
    print('slider2 ' + value)
    return jsonify({'code': 0, 'msg': 'success'})

@app.route('/slider3',methods=['GET'])
def slider3():
    value = request.args['value']
    print('slider3 ' + value)
    return jsonify({'code': 0, 'msg': 'success'})

def gen():
    vid = cv2.VideoCapture(0)
    while True:
        return_value, frame = vid.read()
        image = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

def sen_message(send_message):
    global message
    message = send_message

# sse
def messa():
    global message , old_message
    while True:
        while True:
            if old_message != message:
                yield 'data: {}\n\n'.format(json.dumps({'message': message}))
                break
        old_message = message = ""

@app.route('/stream2')
def stream2():
    return Response(messa(), mimetype="text/event-stream")

if __name__ == '__main__':
    app.run()

# from flask import Flask, render_template
# from flask_socketio import SocketIO
# from threading import Lock
# import random

# async_mode = None
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app, async_mode=async_mode)
# thread = None
# thread_lock = Lock()

# @app.route('/')
# def index():
#     return render_template('index.html', async_mode=socketio.async_mode)

# @socketio.on('connect', namespace='/test_conn')
# def test_connect():
#     global thread
#     with thread_lock:
#         if thread is None:
#             thread = socketio.start_background_task(target=background_thread)

# def background_thread():
#     while True:
#         socketio.sleep(2)
#         t = random.randint(1, 100)
#         socketio.emit('server_response', {'data': t}, namespace='/test_conn')

# @socketio.on('disconnect', namespace='/chat')
# def test_disconnect():
#     print('Client disconnected')

# if __name__ == '__main__':
#     socketio.run(app, debug=True)