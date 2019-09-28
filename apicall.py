import requests
from flask import Flask, flash, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'zomatoapi'

cities = {
        "Bengaluru": 4,
        "Kolkata": 2,
        "Mumbai": 3,
        "Delhi": 1,
        "Pune": 5,
        }


details = {
        "1": 0,
        "2": 0,
        "3": 0,
        "4": 0,
        "5": 0,
        "6": 0,
        "7": 0,
        "8": 0,
        "9": 0,
        "10": 0,
        "11": 0,
        "12": 0,
        "13": 0,
        "14": 0,
        "15": 0,
        "16": 0,
        "17": 0,
        "18": 0,
        "19": 0,
        "20": 0,
        "21": 0,
        "22": 0,
        "23": 0,
        "24": 0
        }
    

bookings = {
            "0": {
                "restidn": 0,
                "timings": details
             }
        }
 


@app.route('/')
def home():
    session['page'] = 0
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    else:
        return 'nothing'

#enter with login credentials as username = admin and password = admin
@app.route('/login', methods=['GET', 'POST'])
def index():
    session['page'] = 0
    print(request.method)
    if request.method == 'GET':
        return render_template("login1.html")
    else:
        name = request.form['username']
        password = request.form['password']

        if name == 'admin' and password == 'admin':
            session['logged_in'] = 'True'
            return redirect(url_for('main'))
        else:
            flash("Wrong Username/Password", "danger")
            return render_template("login1.html")

@app.route('/user')
def main():
    session['page'] = 0
    return render_template("cities.html")

@app.route('/search')
def search():
    session['page'] = 0
    idn = request.args.get('city')
    session['cityid'] = idn

    return render_template('search.html')

#the main route which fetches all restuarants according to filters or no filters
@app.route('/seeall')
def seeall():
    try:
        page = session['page']
        start = page * 10
        count = 20
        print("till here")
        if session.get('city') is None:
            idn = request.args.get('city')
            session['cityid'] = idn

        else:
            idn = session['cityid']

        if 'rname' in request.args:
            rname = request.args['rname']
            count = 20
        else:
            rname = ''

        if 'cuisine' in request.args:
            cuisine = request.args['cuisine']
            count = 20
        else:
            cuisine = ''

        url = "https://developers.zomato.com/api/v2.1/search?entity_id={}&entity_type=city&q={}&start={}&count={}&cuisine={}".format(idn, rname, start, count, cuisine)
        header = {"user_key":"2ae5cb24831540d5abd25a4144301354"}
        response = requests.get(url, headers=header)
        resp = response.json()

        restaurants = resp["restaurants"]
        restuarant_details = []
        i = 0
        for rest in restaurants:
            rest_details = rest["restaurant"]
            restidn = rest_details["id"]
            name = rest_details["name"]
            restid = rest_details["id"]
            url = rest_details["url"]
            loc = rest_details["location"]
            add = loc["address"]
            cuisine = rest_details["cuisines"]
            timing = rest_details["timings"]
            cost = rest_details["average_cost_for_two"]
            r = {
                "restidn": restidn,
                 "name" : name,
                 "url": url,
                 "address": add,
                 "cuisine": cuisine,
                 "timing": timing,
                 "cost": cost,
                 }
            restuarant_details.append(r)
            i += 1

        return render_template("restaurant.html", details = restuarant_details)

    except Exception as e:
        print(e)

    return "SERVER ERROR"


#route to browse through previous and next page
@app.route('/browse')
def prev():
    if 'prev' in request.args:
        page = session['page']
        if page == 0:
            return redirect(url_for('seeall'))
            page -= 1
            session['page'] = page
            return redirect(url_for('seeall'))

    if 'next' in request.args:
        page = session['page']
        page += 1
        session['page'] = page
        return redirect(url_for('seeall'))


#click anywhere on the table of restuarants to initialise booking process
@app.route('/booking')
def booking():
    restidn = request.args['id']
    session['restidn'] = restidn

    return render_template("booking.html")

#click anywhere on the table of restuarants to initialise booking process
@app.route('/bookingcheck')
def bookingcheck():
    people = request.args.get('people')
    time = request.args.get('time')
    people = int(people)
    time = str(time)

    cityidn = session['cityid']
    restidn = session['restidn']
    restidn = str(restidn)

    for booking in bookings:
        print("If condition :", booking)
        print(type(booking))
        print("If condition restidn", restidn)
        if booking == restidn:
            print("Booking : ", booking)
            print("Rest idn : ", restidn)
            timing = (bookings[booking]['timings'])
            print("Timing booking ", timing[time])
            p1 = timing[time] 
            p1 = p1 + people
            if p1 > 20 :
                return "Booking limit exceeded!"
            else:
                timing[time] = p1
                return "Thanks for booking"

    d = details
    d[time] = d[time] + people

    print("New deets : ", d)

    b =  {
            'timings': d
            }
    bookings[restidn] = b

    return "Thanks for booking" 


if __name__ == "__main__":
    app.run(host='0.0.0.0')
