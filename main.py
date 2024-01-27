# وارد کردن ماژول sqlite3
import sqlite3

# ایجاد یک اتصال به دیتابیس
conn = sqlite3.connect('jobs.db')

# ایجاد یک شیء cursor برای اجرای پرسمان‌ها
cur = conn.cursor()

# ایجاد جدول user با ستون‌های username، password، birthdate، resume و interests
cur.execute('''
CREATE TABLE user (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    birthdate DATE NOT NULL,
    resume TEXT,
    interests TEXT
)
''')

# ایجاد جدول company با ستون‌های company_id، company_name و company_address
cur.execute('''
CREATE TABLE company (
    company_id INTEGER PRIMARY KEY,
    company_name TEXT NOT NULL,
    company_address TEXT
)
''')

# ایجاد جدول jobs با ستون‌های job_id، job_title، job_description، company_id و salary
cur.execute('''
CREATE TABLE jobs (
    job_id INTEGER PRIMARY KEY,
    job_title TEXT NOT NULL,
    job_description TEXT,
    company_id INTEGER NOT NULL,
    salary REAL,
    FOREIGN KEY (company_id) REFERENCES company (company_id)
)
''')

# درج چند رکورد نمونه در جدول user
cur.execute('''
INSERT INTO user (username, password, birthdate, resume, interests)
VALUES
('ali', '1234', '1990-01-01', 'I am a software engineer with 5 years of experience.', 'programming, reading, music'),
('sara', '5678', '1992-02-02', 'I am a graphic designer with 3 years of experience.', 'design, art, photography'),
('reza', 'abcd', '1994-03-03', 'I am a data analyst with 2 years of experience.', 'data, statistics, machine learning')
''')

# درج چند رکورد نمونه در جدول company
cur.execute('''
INSERT INTO company (company_name, company_address)
VALUES
('ABC', 'Tehran, Iran'),
('XYZ', 'Shiraz, Iran'),
('LMN', 'Isfahan, Iran')
''')

# درج چند رکورد نمونه در جدول jobs
cur.execute('''
INSERT INTO jobs (job_title, job_description, company_id, salary)
VALUES
('Software Developer', 'Develop web and mobile applications using Python, Django and React.', 1, 2000.0),
('Graphic Designer', 'Create logos, flyers and posters using Photoshop and Illustrator.', 2, 1500.0),
('Data Scientist', 'Analyze and visualize data using Python, Pandas and Matplotlib.', 3, 2500.0)
''')

# ذخیره تغییرات در دیتابیس
conn.commit()

# اجرای چند پرسمان نمونه

# پرسمان 1: نمایش نام، رزومه و علایق کاربرانی که علاقه به برنامه‌نویسی دارند
cur.execute('''
SELECT username, resume, interests
FROM user
WHERE interests LIKE '%programming%'
''')
print('Users who are interested in programming:')
for row in cur:
    print(row)

# پرسمان 2: نمایش عنوان شغل، نام شرکت و حقوق شغل‌هایی که حقوق بیش از 2000 دلار دارند
cur.execute('''
SELECT job_title, company_name, salary
FROM jobs
JOIN company ON jobs.company_id = company.company_id
WHERE salary > 2000
''')
print('Jobs with salary more than 2000:')
for row in cur:
    print(row)

# بستن اتصال به دیتابیس
conn.close()