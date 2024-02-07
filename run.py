from app import app, db

if __name__ == '__main__':
    db_path = 'varastonhallinta/varastonhallinta.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    db.create_all()
    app.run(debug=True)
