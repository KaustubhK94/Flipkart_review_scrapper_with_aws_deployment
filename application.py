from werkzeug.utils import send_file
from flask import Flask, render_template, request,session
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import csv
import io

# By beanstalk convention
application = Flask(__name__)
app = application
app.secret_key = "super secret key"

@app.route('/', methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/review', methods=['POST', 'GET']) # route to show the review comments in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ","")
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString
            uClient = uReq(flipkart_url)
            flipkartPage = uClient.read()
            uClient.close()
            flipkart_html = bs(flipkartPage, "html.parser")
            bigboxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"})
            del bigboxes[0:3]
            box = bigboxes[0]
            productLink = "https://www.flipkart.com" + box.div.div.div.a['href']
            prodRes = requests.get(productLink)
            prodRes.encoding='utf-8'
            prod_html = bs(prodRes.text, "html.parser")
            # print(prod_html)
            commentboxes = prod_html.find_all('div', {'class': "_16PBlm"})
            print(commentboxes)
            filename = searchString + ".csv"
            fw = open(filename, "w", encoding="UTF8")
            headers = "Product, Customer Name, Rating, Heading, Comment\n"
            fw.write(headers)
            reviews = []
            for commentbox in commentboxes:
                try:
                    name = commentbox.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text
                except:
                    name = 'No Name'
                try:
                    rating = commentbox.div.div.div.div.text
                except:
                    rating = 'No Rating'
                try:
                    commentHead = commentbox.div.div.div.p.text

                except:
                    commentHead = 'No Comment Heading'
                try:
                    comtag = commentbox.div.div.find_all('div', {'class': ''})
                    custComment = comtag[0].div.text
                except Exception as e:
                    print("Exception while creating dictionary: ", e)
                mydict = {"Product": searchString, "Customer Name": name, "Rating": rating, "Heading": commentHead,
                          "Comment": custComment}
                reviews.append(mydict)
                writer = csv.writer(fw)
                writer.writerow(list(mydict.values()))
            session["filename"] = filename
            session["reviews"] = reviews[0:(len(reviews)-1)]
            return render_template('results.html', reviews=session["reviews"])
        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong'
    else:
        return render_template('index.html')

@app.route("/download", methods=["POST"])
def download():
    csv = session["df"] if "df" in session else ""
    if csv == "":
        return "No data found to download"
    else:
        buf_str = io.StringIO(csv)
        buf_byt = io.BytesIO(buf_str.read().encode("utf-8"))
        return send_file(buf_byt, mimetype="text/csv", as_attachment=True,environ=request.environ,download_name="session.csv")

if __name__ == "__main__":
	app.run(debug=True)


