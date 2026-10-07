from flask import Flask, request, jsonify, render_template_string
import json
import os
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)

# =========================================================
# SETTINGS
# =========================================================

DATA_FILE = "students.json"
UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# =========================================================
# DATA FUNCTIONS
# =========================================================

def load_data():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except:
        return []


def save_data(students):
    with open(DATA_FILE, "w") as file:
        json.dump(students, file, indent=4)


# =========================================================
# FRONTEND - HTML + CSS + JAVASCRIPT
# =========================================================

HTML = """
<!DOCTYPE html>

<html>

<head>

    <title>Student Management System</title>

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <style>

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #eef2f7;
        }

        .container {
            width: 1100px;
            max-width: 95%;
            margin: 30px auto;
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 25px rgba(0,0,0,0.15);
        }

        h1 {
            text-align: center;
            margin-bottom: 25px;
        }

        .form-section {
            display: flex;
            gap: 35px;
            margin-bottom: 20px;
        }

        .image-section {
            width: 190px;
            text-align: center;
        }

        #imagePreview {
            width: 150px;
            height: 150px;
            object-fit: cover;
            border-radius: 12px;
            border: 2px solid #ccc;
            margin-bottom: 10px;
        }

        .form {
            flex: 1;

            display: grid;

            grid-template-columns: 120px 1fr;

            gap: 12px;

            align-items: center;
        }

        .form label {
            font-weight: bold;
        }

        .form input {
            padding: 11px;

            border: 1px solid #ccc;

            border-radius: 7px;

            font-size: 15px;
        }

        .buttons {
            display: flex;

            gap: 10px;

            flex-wrap: wrap;

            margin: 20px 0;
        }

        button {
            border: none;

            padding: 11px 22px;

            border-radius: 7px;

            background: #2563eb;

            color: white;

            cursor: pointer;

            font-size: 14px;

            font-weight: bold;
        }

        button:hover {
            background: #1d4ed8;
        }

        .delete-btn {
            background: #dc2626;
        }

        .delete-btn:hover {
            background: #b91c1c;
        }

        .clear-btn {
            background: #64748b;
        }

        .clear-btn:hover {
            background: #475569;
        }

        #message {
            margin: 15px 0;

            font-weight: bold;

            min-height: 20px;
        }

        table {
            width: 100%;

            border-collapse: collapse;

            margin-top: 15px;
        }

        th,
        td {
            border: 1px solid #ddd;

            padding: 10px;

            text-align: center;
        }

        th {
            background: #2563eb;

            color: white;
        }

        tr:hover {
            background: #f1f5f9;

            cursor: pointer;
        }

        .student-image {
            width: 55px;

            height: 55px;

            object-fit: cover;

            border-radius: 50%;

            border: 2px solid #ddd;
        }

        @media(max-width: 700px) {

            .form-section {
                flex-direction: column;
            }

            .image-section {
                width: 100%;
            }

            .form {
                grid-template-columns: 1fr;
            }

            table {
                font-size: 12px;
            }

        }

    </style>

</head>


<body>


<div class="container">

    <h1>
        Student Management System
    </h1>


    <!-- ================= FORM ================= -->

    <div class="form-section">


        <!-- IMAGE -->

        <div class="image-section">

            <img id="imagePreview"
                 src="https://via.placeholder.com/150"
                 alt="Student Image">

            <br>

            <input type="file"
                   id="image"
                   accept="image/*">

        </div>


        <!-- INPUTS -->

        <div class="form">

            <label>
                Roll No
            </label>

            <input
                type="text"
                id="roll"
                placeholder="Enter Roll No"
            >


            <label>
                Name
            </label>

            <input
                type="text"
                id="name"
                placeholder="Enter Student Name"
            >


            <label>
                Course
            </label>

            <input
                type="text"
                id="course"
                placeholder="Enter Course"
            >


            <label>
                Marks
            </label>

            <input
                type="number"
                id="marks"
                placeholder="Enter Marks"
                min="0"
                max="100"
            >

        </div>

    </div>


    <!-- ================= BUTTONS ================= -->

    <div class="buttons">

        <button onclick="addStudent()">
            Add
        </button>

        <button onclick="updateStudent()">
            Update
        </button>

        <button
            class="delete-btn"
            onclick="deleteStudent()">

            Delete

        </button>

        <button onclick="searchStudent()">
            Search
        </button>

        <button
            class="clear-btn"
            onclick="clearForm()">

            Clear

        </button>

        <button onclick="loadStudents()">
            Show All
        </button>

    </div>


    <div id="message"></div>


    <!-- ================= TABLE ================= -->

    <table>

        <thead>

            <tr>

                <th>
                    Image
                </th>

                <th>
                    Roll No
                </th>

                <th>
                    Name
                </th>

                <th>
                    Course
                </th>

                <th>
                    Marks
                </th>

            </tr>

        </thead>


        <tbody id="studentTable">

        </tbody>

    </table>


</div>


<script>

/* =========================================================
   IMAGE PREVIEW
   ========================================================= */

document
.getElementById("image")
.addEventListener("change", function() {

    const file = this.files[0];

    if (!file) {
        return;
    }

    const reader = new FileReader();

    reader.onload = function(event) {

        document
        .getElementById("imagePreview")
        .src = event.target.result;

    };

    reader.readAsDataURL(file);

});


/* =========================================================
   MESSAGE
   ========================================================= */

function showMessage(message, success = true) {

    const box =
        document.getElementById("message");

    box.innerText = message;

    if (success) {

        box.style.color = "green";

    } else {

        box.style.color = "red";

    }

}


/* =========================================================
   ADD STUDENT
   ========================================================= */

async function addStudent() {

    const roll =
        document.getElementById("roll").value.trim();

    const name =
        document.getElementById("name").value.trim();

    const course =
        document.getElementById("course").value.trim();

    const marks =
        document.getElementById("marks").value.trim();

    if (!roll || !name || !course || !marks) {

        showMessage(
            "Please fill all fields.",
            false
        );

        return;
    }


    const formData = new FormData();

    formData.append("roll", roll);

    formData.append("name", name);

    formData.append("course", course);

    formData.append("marks", marks);


    const image =
        document.getElementById("image").files[0];

    if (image) {

        formData.append("image", image);

    }


    const response =
        await fetch(
            "/api/students",
            {
                method: "POST",
                body: formData
            }
        );


    const data =
        await response.json();


    showMessage(
        data.message,
        data.success
    );


    if (data.success) {

        clearForm();

        loadStudents();

    }

}


/* =========================================================
   LOAD STUDENTS
   ========================================================= */

async function loadStudents() {

    const response =
        await fetch("/api/students");


    const students =
        await response.json();


    const table =
        document.getElementById("studentTable");


    table.innerHTML = "";


    students.forEach(student => {

        const row =
            document.createElement("tr");


        const image =
            student.Image
            ? student.Image
            : "https://via.placeholder.com/150";


        row.innerHTML = `

            <td>

                <img
                    src="${image}"
                    class="student-image"
                >

            </td>

            <td>
                ${student.Roll}
            </td>

            <td>
                ${student.Name}
            </td>

            <td>
                ${student.Course}
            </td>

            <td>
                ${student.Marks}
            </td>

        `;


        row.onclick = function() {

            document.getElementById("roll")
                .value = student.Roll;

            document.getElementById("name")
                .value = student.Name;

            document.getElementById("course")
                .value = student.Course;

            document.getElementById("marks")
                .value = student.Marks;


            document.getElementById("imagePreview")
                .src =
                student.Image ||
                "https://via.placeholder.com/150";

        };


        table.appendChild(row);

    });

}


/* =========================================================
   UPDATE STUDENT
   ========================================================= */

async function updateStudent() {

    const roll =
        document.getElementById("roll").value.trim();


    if (!roll) {

        showMessage(
            "Enter Roll No first.",
            false
        );

        return;
    }


    const formData =
        new FormData();


    formData.append(
        "name",
        document.getElementById("name").value.trim()
    );


    formData.append(
        "course",
        document.getElementById("course").value.trim()
    );


    formData.append(
        "marks",
        document.getElementById("marks").value.trim()
    );


    const image =
        document.getElementById("image").files[0];


    if (image) {

        formData.append(
            "image",
            image
        );

    }


    const response =
        await fetch(
            "/api/students/" + roll,
            {
                method: "PUT",
                body: formData
            }
        );


    const data =
        await response.json();


    showMessage(
        data.message,
        data.success
    );


    if (data.success) {

        clearForm();

        loadStudents();

    }

}


/* =========================================================
   DELETE STUDENT
   ========================================================= */

async function deleteStudent() {

    const roll =
        document.getElementById("roll").value.trim();


    if (!roll) {

        showMessage(
            "Enter Roll No first.",
            false
        );

        return;
    }


    const confirmDelete =
        confirm(
            "Delete student with Roll No " +
            roll +
            "?"
        );


    if (!confirmDelete) {

        return;

    }


    const response =
        await fetch(
            "/api/students/" + roll,
            {
                method: "DELETE"
            }
        );


    const data =
        await response.json();


    showMessage(
        data.message,
        data.success
    );


    if (data.success) {

        clearForm();

        loadStudents();

    }

}


/* =========================================================
   SEARCH STUDENT
   ========================================================= */

async function searchStudent() {

    const roll =
        document.getElementById("roll").value.trim();


    if (!roll) {

        showMessage(
            "Enter Roll No to search.",
            false
        );

        return;
    }


    const response =
        await fetch(
            "/api/students/search/" + roll
        );


    const data =
        await response.json();


    if (!data.success) {

        showMessage(
            data.message,
            false
        );

        return;
    }


    const student =
        data.student;


    document.getElementById("name")
        .value = student.Name;


    document.getElementById("course")
        .value = student.Course;


    document.getElementById("marks")
        .value = student.Marks;


    document.getElementById("imagePreview")
        .src =
        student.Image ||
        "https://via.placeholder.com/150";


    showMessage(
        "Student Found!",
        true
    );

}


/* =========================================================
   CLEAR
   ========================================================= */

function clearForm() {

    document.getElementById("roll")
        .value = "";

    document.getElementById("name")
        .value = "";

    document.getElementById("course")
        .value = "";

    document.getElementById("marks")
        .value = "";

    document.getElementById("image")
        .value = "";

    document.getElementById("imagePreview")
        .src =
        "https://via.placeholder.com/150";

    document.getElementById("message")
        .innerText = "";

}


/* =========================================================
   LOAD DATA WHEN PAGE OPENS
   ========================================================= */

loadStudents();

</script>


</body>

</html>
"""


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    return render_template_string(HTML)


# =========================================================
# GET ALL STUDENTS
# =========================================================

@app.route("/api/students", methods=["GET"])
def get_students():

    return jsonify(load_data())


# =========================================================
# ADD STUDENT
# =========================================================

@app.route("/api/students", methods=["POST"])
def add_student():

    roll = request.form.get(
        "roll",
        ""
    ).strip()

    name = request.form.get(
        "name",
        ""
    ).strip()

    course = request.form.get(
        "course",
        ""
    ).strip()

    marks = request.form.get(
        "marks",
        ""
    ).strip()


    if not roll or not name or not course or not marks:

        return jsonify({
            "success": False,
            "message": "Please fill all fields."
        }), 400


    students = load_data()


    # Duplicate Roll Number

    for student in students:

        if student["Roll"] == roll:

            return jsonify({
                "success": False,
                "message": "Roll No already exists."
            }), 400


    # Image

    image_url = ""


    image = request.files.get("image")


    if image and image.filename:

        extension = os.path.splitext(
            secure_filename(image.filename)
        )[1]


        filename = (
            str(uuid.uuid4())
            + extension
        )


        image_path = os.path.join(
            UPLOAD_FOLDER,
            filename
        )


        image.save(image_path)


        image_url = "/uploads/" + filename


    student = {

        "Roll": roll,

        "Name": name,

        "Course": course,

        "Marks": marks,

        "Image": image_url

    }


    students.append(student)


    save_data(students)


    return jsonify({

        "success": True,

        "message":
        "Student Added Successfully!"

    })


# =========================================================
# UPDATE STUDENT
# =========================================================

@app.route(
    "/api/students/<roll>",
    methods=["PUT"]
)
def update_student(roll):

    students = load_data()


    student_found = None


    for student in students:

        if student["Roll"] == roll:

            student_found = student

            break


    if not student_found:

        return jsonify({

            "success": False,

            "message":
            "Student Not Found!"

        }), 404


    student_found["Name"] = request.form.get(
        "name",
        student_found["Name"]
    ).strip()


    student_found["Course"] = request.form.get(
        "course",
        student_found["Course"]
    ).strip()


    student_found["Marks"] = request.form.get(
        "marks",
        student_found["Marks"]
    ).strip()


    image = request.files.get("image")


    if image and image.filename:

        extension = os.path.splitext(
            secure_filename(image.filename)
        )[1]


        filename = (
            str(uuid.uuid4())
            + extension
        )


        image_path = os.path.join(
            UPLOAD_FOLDER,
            filename
        )


        image.save(image_path)


        student_found["Image"] = "/uploads/" + filename


    save_data(students)


    return jsonify({

        "success": True,

        "message":
        "Record Updated Successfully!"

    })


# =========================================================
# DELETE STUDENT
# =========================================================

@app.route(
    "/api/students/<roll>",
    methods=["DELETE"]
)
def delete_student(roll):

    students = load_data()


    new_students = []


    deleted = False


    for student in students:

        if student["Roll"] == roll:

            deleted = True


            # Delete image

            image = student.get(
                "Image",
                ""
            )


            if image:

                image_path = image.lstrip("/")


                if os.path.exists(
                    image_path
                ):

                    os.remove(
                        image_path
                    )

        else:

            new_students.append(
                student
            )


    if not deleted:

        return jsonify({

            "success": False,

            "message":
            "Student Not Found!"

        }), 404


    save_data(new_students)


    return jsonify({

        "success": True,

        "message":
        "Record Deleted Successfully!"

    })


# =========================================================
# SEARCH STUDENT
# =========================================================

@app.route(
    "/api/students/search/<roll>",
    methods=["GET"]
)
def search_student(roll):

    students = load_data()


    for student in students:

        if student["Roll"] == roll:

            return jsonify({

                "success": True,

                "student": student

            })


    return jsonify({

        "success": False,

        "message":
        "Student Not Found!"

    }), 404


# =========================================================
# SERVE UPLOADED IMAGES
# =========================================================

@app.route("/uploads/<filename>")
def uploaded_file(filename):

    from flask import send_from_directory

    return send_from_directory(
        UPLOAD_FOLDER,
        filename
    )


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    print()
    print("======================================")
    print(" STUDENT MANAGEMENT SYSTEM")
    print("======================================")
    print()
    print("Server running at:")
    print("http://127.0.0.1:5000")
    print()

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )
