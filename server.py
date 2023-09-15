from flask import Flask, render_template
import boto3
from boto3.dynamodb.conditions import Key
import random
import os

app = Flask(__name__)

visitors = 0
ddb_resource = boto3.resource('dynamodb', region_name='ap-southeast-1')
table_name = os.environ.get('JOKES_NAME')
table = ddb_resource.Table(table_name)

@app.route("/mem")
def mem():
    global visitors
    visitors += 1
    return f"Hello, visitor #{visitors}! Get ready to laugh!"

@app.route("/ddb")
def ddb():    
    populate_table()
    joke = tell_joke()
    return render_template('jokes.html', question=joke['Question'], answer=joke['Answer'])

def populate_table():
    with table.batch_writer() as batch:
        batch.put_item(Item={"Number": 1, "Question": "What's brown and sticky?", "Answer": "A stick!"})
        batch.put_item(Item={"Number": 2, "Question": "What's orange and sounds like a parrot?", "Answer": "A carrot!"})
        batch.put_item(Item={"Number": 3, "Question": "Why was six afraid of seven?", "Answer": "Because seven ate nine!"})
        batch.put_item(Item={"Number": 4, "Question": "What's a cucumber's favorite instrument?", "Answer": "A pickle-o!"})
        batch.put_item(Item={"Number": 5, "Question": "Why don't seagulls fly over the bay?", "Answer": "Because then they'd be bagels!"})
        batch.put_item(Item={"Number": 6, "Question": "What did the baker say after they sold out of pita bread?", "Answer": "We have naan!"})
        batch.put_item(Item={"Number": 7, "Question": "What did the robber take from the music store?", "Answer": "The lute!"})
        batch.put_item(Item={"Number": 8, "Question": "If April showers bring May flowers, what do Mayflowers bring?", "Answer": "Pilgrims!"})
        batch.put_item(Item={"Number": 9, "Question": "How much soda do tropical birds drink?", "Answer": "Toucans!"})
        batch.put_item(Item={"Number": 10, "Question": "How many tickles does it take to tickle an octopus?", "Answer": "TENtacles!"})
        batch.put_item(Item={"Number": 11, "Question": "What do you call a factory that makes only acceptable?", "Answer": "A satisFACTORY!"})
    return "done populating table"

def tell_joke():
    jokeNumber = random.randint(1, 11)
    table = ddb_resource.Table(table_name)
    try: 
        resp = table.get_item(Key={"Number": jokeNumber})
    except Exception as e:
        print(e.response['Error']['Message'])
    else:
        return resp['Item']

@app.route("/")
def home():
    return "Visit /ddb for some belly laughs or /mem to be reminded of '90s-era web counters."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)