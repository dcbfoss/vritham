#!/usr/bin/python3
import cgi, sys, codecs
import cgitb  
import sqlite3

cgitb.enable(display=0)
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

titlebar = """
 <div class="page-header">
        <a href="https://kavyanarthaki.in/"><img class="logo-image" src="https://kavyanarthaki.in/assets/Logo_of_University_of_Kerala.png" alt="UOK"></a>
        <div class="header-text">
            <h1>കാവ്യനർത്തകി</h1>
            <h2 class="subheading">(Based on Kavyanarthaki Python package for Malayalam Meters)</h2>
            <h3 class="subheading">Developed by Machine Learning Team of Dept of Computational Biology & Bioinformatics, University of Kerala.</h3>
        </div>
 </div>
 <center>
    <div class="menuitems">
        <a href="https://colab.research.google.com/drive/1BXRAZ-E5SckC6094gU2XWFuXLxnbJbP7?usp=sharing"><img data-canonical-src="https://kavyanarthaki.in/assets/colab-badge.svg" alt="Open In Colab" src="https://kavyanarthaki.in/assets/colab-badge2.svg" width="234" height="40"></a>
        <a href="https://www.google.com/intl/ml/inputtools/try/"><img data-canonical-src="https://kavyanarthaki.in/assets/google_inputtool_logo.png" alt="Open In Colab" src="https://kavyanarthaki.in/assets/google_inputtool_logo.png"  width="234" height="40"></a>
        <img id="kavyaexamples" data-canonical-src="https://kavyanarthaki.in/assets/example_logo.png" alt="Open In Colab" src="https://kavyanarthaki.in/assets/example_logo.png"  width="234" height="40">
    </div>
</center>
"""
postloadscripts = """
<script>
document.getElementById("kavyaexamples").onclick = function(){
            const form = document.createElement('form');
            form.method = "POST";
            form.action = "https://kavyanarthaki.in/cgi-bin/index.cgi";
            const op = document.createElement('input');
            op.type = 'hidden';op.name = "analysis";op.value = 'ex';
            const dt = document.createElement('input');
            dt.type = 'hidden';dt.name = "data";dt.value = "ഉദാഹരണം";
            form.appendChild(op);form.appendChild(dt);
            document.body.appendChild(form);form.submit();
            form.remove();
        };
</script>
"""
footer = """
<footer>
<div class="subfooter0" id="subfooter1">
<center><div class="subfooter2"><img src="https://kavyanarthaki.in/assets/logo_m.png" alt="Kavyanarthaki" width="100" height="100"></div></center>
<div class="subfooter2"><button class="backbutton" onclick="history.back()">തിരിച്ചു  പോകാം</button></div></div>
<div class="subfooter">
<div class="aboutcard"><u>About</u><br>This website and associated code is maintained by machine learning team of Dept of Computational Biology and Bio-informatics, University of Kerala.&nbsp;<a href="https://kavyanarthaki.in/cgi-bin/stats.cgi">See Statistics.</a></div>
<div class="contactcard"><u>Contact details</u><br>For enquiry related to kavyanarthaki: <a href="mailto:neenumohan1998@gmail.com">neenumohan1998@gmail.com</a>, <a href="mailto:sankar.achuth@gmail.com">sankar.achuth@gmail.com</a><br>
For technical related enquiries and suggestions: <a href="mailto:mpvinod625@gmail.com">mpvinod625@gmail.com</a></div>
</div>
<div class="subfooter0">For background reading: 1. Article in Vijnana Kairali (2022),  2. Malayalam Meter- A modern Pedagogic Introduction (Forthcoming-2022), 3. Kavyanarthaki Package Documentation</div
</footer>
"""

def getchartscript(data):
    labels = {'gurulaghu':'ഗുരു ലഘു നോക്കിയത്.','basha':'ഭാഷാ വൃത്ത പരിശോധന.','sanskrit':'സംസ്‌കൃത  വൃത്ത പരിശോധന.','mixed':'ഭാഷാ/സംസ്‌കൃത  വൃത്ത പരിശോധന.','summary':'അപഗ്രഥനസംഗ്രഹം നോക്കിയത്.','vaythari':'വായ്ത്താരി നോക്കിയത്.'}
    output = """<script type="text/javascript">
    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(drawChart);
    function drawChart() {
    var data = google.visualization.arrayToDataTable([['Analysis', 'Count'],"""
    for j, i in enumerate(data.keys()):
        if (j < (len(data.keys())-1)):
            output = output + "['"+labels[i]+"',"+str(data[i])+"],"
        else:
            output = output + "['"+labels[i]+"',"+str(data[i])+"]"
    output = output + """]);
    var options = {'title':'Usage Statistics', 'width':550, 'height':400};
    var chart = new google.visualization.PieChart(document.getElementById('piechart'));
    chart.draw(data, options);
    }</script>"""
    return output

print("Content-type:text/html\r\n")
print('<!DOCTYPE html>')
print('<html lang="ml"><head>')
print('<meta charset="UTF-8">')
print('<meta name="description" content="Website that aid study in analysing malayalam meters.">')
print('<meta name="keywords" content="malayalam meters, malayalam, meters, analysis">')
print('<meta name="author" content="Prof. Achuthsankar S Nair">')
print('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
print('<link rel="icon" type="image/x-icon" href="https://kavyanarthaki.in/assets/logo.ico">')
print('<link rel="stylesheet" href="https://kavyanarthaki.in/assets/kavya_style.css">')
print('<title>കാവ്യനർത്തകി</title></head><body>')

try:
    entries = {};count = 0;
    with sqlite3.connect('comments.db') as sqliteConnection:
        cursor = sqliteConnection.cursor()
        data = cursor.execute("SELECT action, COUNT(*) AS 'num' FROM kavyapoems GROUP BY action;").fetchall()
        for i in data:
            entries[i[0]] = int(i[1])
        data = cursor.execute("SELECT COUNT(DISTINCT data) FROM kavyapoems;").fetchall()
        count = data[0][0]
        
except Exception as e:
    data = 'error'

print(titlebar)
print('<center><div id="maincontainer">')
print("<H1 class='highlight'>","ഇത് വരെ ",count, "കവിതകൾ പരിശോധിച്ചു.","</H1>")
print('<div id="piechart"></div>')
print('<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>')
print(getchartscript(entries))
print('</div></center>')
print(postloadscripts)
print(footer)
print('</body></html>')