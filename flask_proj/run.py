from flaskblog import app,db


if __name__ == "__main__":
  with app.app_context(): #this part creates our db once we run the script
    db.create_all()
  app.run(debug=True) #reloads after any changes