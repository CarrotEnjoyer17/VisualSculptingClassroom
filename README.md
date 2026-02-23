### Description
Visual Sculpting Classroom - site, created for uploading, watching and marking 3d models, created by students. As mentioned, project created for students and teachers if 3d modeling courses, therefore it has classrooms system, marking, commenting and moderating features.

### Basic usage

##### 1. Roles:
Every user can register one or more accounts on one email or login with different roles. Platform supprots following roles:
- Student - can join classes and upload models
- Teacher - can create and classes, mark works and leave marks for them, also have admin rights in classrooms made by them
- Admin - can join classes, delete users and their works from them

##### 2. Classrooms:
Classrooms allow to unite group of students, teachers and admins in one structure. Classes may be created only by the teachers, after that the classroom is getting a random generated number, by which any user can join classroom. The teacher, who created classroom have all the admin rights, but cant be deleted by admin, and has a right to delete other admins.
In classrooms, students can upload their 3d models, which will be displayed only in that classroom for teachers. Any teacher can leave a mark and a comment to any students work. Using all the marks, platform counts the average mark for a student in that classroom.
Every uploaded model can be seen in the classroom in real time, which also allow to rotate and scale them, without downloading them or leaving site.

##### 3. Profile:
Every user chooses his name, when registering a new account. Later, name can be changed in profile section on platform, also avatar and password can be edited.

### Stack:

1. Main language(for backend) - Python and Django framework
2. Assistive languages(for frontend and 3d models watching) - HTML, CSS, JavaScript and Three.js framework
3. Database: Lite SQL
