import sqlite3

# ایجاد یک اتصال به فایل دیتابیس
conn = sqlite3.connect("person.db")

# ایجاد یک شیء cursor برای اجرای دستورات SQL
cur = conn.cursor()

# ایجاد یک جدول با نام person
cur.execute("CREATE TABLE IF NOT EXISTS person (username TEXT, password TEXT, membership_date TEXT,membership_date_expire TEXT , interests TEXT)")

# دریافت اطلاعات شخص از ورودی کاربر
username = input("نام کاربری را وارد کنید: ")
password = input("رمز عبور را وارد کنید: ")
membership_date = input("تاریخ عضویت را وارد کنید: ")
membership_date_expire = input("تاریخ مهلت اتمام دسترسی را وارد کنید: ")
interests = input("علایق وارد کنید: ")

# افزودن اطلاعات شخص به جدول person
cur.execute("INSERT INTO person VALUES (?, ?, ?, ?,?)", (username, password, membership_date,membership_date_expire, interests))

# ذخیره تغییرات در دیتابیس
conn.commit()

# بستن اتصال به دیتابیس
conn.close()

# چاپ پیام موفقیت
print("اطلاعات شخص با موفقیت ذخیره شد.")