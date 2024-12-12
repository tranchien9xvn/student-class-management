from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Danh sách học sinh và điểm
name_list = ["Alex", "Jack", "Steve", "Bill", "Thay Chien", "Quan"]
score_list = [10, 7.5, 8, 9, 10, 0]

@app.route('/')
def home():
    # Tạo một danh sách các tuple (tên, điểm)
    students = list(zip(name_list, score_list)) 
    return render_template('index.html', students=students)
'''
@app.route('/')
def home():
    # Kết hợp name_list và score_list thành một danh sách của tuple (name, score)
    students = list(zip(name_list, score_list))
    return render_template('index.html', students=students)
'''

@app.route('/class_size')
def class_size():
    size = len(name_list)
    return render_template('class_size.html', size=size)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        # Lấy thông tin từ form
        new_name = request.form.get('name')
        new_score = float(request.form.get('score'))
        
        # Thêm học sinh vào danh sách
        name_list.append(new_name)
        score_list.append(new_score)
        
        # Chuyển hướng về trang chủ sau khi thêm
        return redirect(url_for('home'))

    # Nếu là GET request, hiển thị form thêm học sinh
    return render_template('add_student.html')

@app.route('/remove_student', methods=['GET', 'POST'])
def remove_student():
    if request.method == 'POST':
        student_remove = request.form.get('name')
        
        # Kiểm tra xem học sinh có tồn tại trong danh sách không
        if student_remove in name_list:
            index = name_list.index(student_remove)
            # Xóa học sinh và điểm của học sinh khỏi danh sách
            name_list.pop(index)
            score_list.pop(index)
            message = f"You have removed {student_remove} from the class."
        else:
            message = "Error: student does not exist in the list."

        return render_template('remove_student.html', message=message)

    # Nếu là GET request, hiển thị form để nhập tên học sinh cần xóa
    return render_template('remove_student.html')

@app.route('/score_update', methods=['GET', 'POST'])
def score_update():
    if request.method == 'POST':
        student_name = request.form.get('name')
        new_score = request.form.get('score')
        
        # Kiểm tra xem tên học sinh có tồn tại trong danh sách không
        if student_name in name_list:
            index = name_list.index(student_name)
            # Cập nhật điểm mới
            score_list[index] = float(new_score)
            message = f"Updated {student_name}'s score to {new_score}."
        else:
            message = "Error: student does not exist in the list."

        return render_template('score_update.html', message=message)

    # Nếu là GET request, hiển thị form để người dùng nhập tên học sinh và điểm mới
    return render_template('score_update.html')


@app.route('/max_score')
def max_score():
    if len(score_list) == 0:
        return render_template('max_score.html', message="No students in the class.")

    max_score = max(score_list)
    max_students = []

    # Tìm các học sinh có điểm cao nhất
    for i in range(len(score_list)):
        if score_list[i] == max_score:
            max_students.append(name_list[i])

    return render_template('max_score.html', max_score=max_score, max_students=max_students)


@app.route('/min_score')
def min_score():
    min_score = min(score_list)
    lowest_students = [name_list[i] for i in range(len(score_list)) if score_list[i] == min_score]
    return render_template('min_score.html', min_score=min_score, lowest_students=lowest_students)

if __name__ == '__main__':
    app.run(debug=True)
