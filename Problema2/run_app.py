from app import app
import sys

if len(sys.argv)!=5:
	print("uso:", sys.argv[0], "host port serverhost serverport")
	sys.exit(1)
HOST=sys.argv[1]
PORT=sys.argv[2]
app.run(debug=True,host=HOST,port=PORT)
