from flask import Flask, request, render_template_string, jsonify
import logging

app = Flask(__name__)

# Burada index.php içeriğini HTML olarak direkt template string yapacağız.
# index_php_html değişkeni içine senin gönderdiğin HTML kodunu koyacağız.

index_php_html = """<!DOCTYPE html>
<html lang="en">
 <head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="title" content="CC Checker - Free credit card checker namso-gen.eu.org" />
  <meta name="description" content="cc checker for free credit card numbers." />
  <meta name="keywords" content="cc,checker,mass cc checker,bin,generated cc,credit card,live,dead" />
  <meta name="robots" content="index, follow" />
  <meta name="language" content="English" />
  <meta name="author" content="Saksham" />
  <meta property="og:url" content="https://namso-gen.eu.org" />
  <meta property="og:image" content="https://rawcdn.githack.com/OshekharO/Entertainment-Index/17d005915d5e20780a46aef227f08367ca8efb3a/img/apple-touch-icon.png" />
  <meta property="og:locale" content="en_US" />
  <meta property="og:type" content="website" />
  <meta name="copyright" content="Copyright © 2023 OshekharO" />
  <meta property="og:image" content="https://rawcdn.githack.com/OshekharO/Entertainment-Index/17d005915d5e20780a46aef227f08367ca8efb3a/img/android-chrome-512x512.png" />
  <link rel="shortcut icon" href="https://rawcdn.githack.com/OshekharO/Entertainment-Index/17d005915d5e20780a46aef227f08367ca8efb3a/img/favicon.ico" type="image/x-icon" />
  <link rel="apple-touch-icon" sizes="180x180" href="https://rawcdn.githack.com/OshekharO/Entertainment-Index/17d005915d5e20780a46aef227f08367ca8efb3a/img/apple-touch-icon.png" />
  <link rel="icon" type="image/png" href="https://rawcdn.githack.com/OshekharO/Entertainment-Index/17d005915d5e20780a46aef227f08367ca8efb3a/img/favicon-32x32.png" sizes="32x32" />
  <link rel="icon" type="image/png" href="https://github.com/OshekharO/Entertainment-Index/blob/master/img/favicon-16x16.png" sizes="16x16" />
  <title>CHECKER CC</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet" crossorigin="anonymous" />
  <link href="style.css" rel="stylesheet" />
 </head>

 <body>
  <div class="fs-3 fw-bold mb-5 text-uppercase mx-auto text-center text-light">Credit Card Checker</div>
  <form method="post" action="/api" role="form" id="form">
   <div class="box-body">
    <div class="box-content">
     <label for="cc" class="form-label fs-6 font-monospace badge bg-danger text-light">Card Numbers</label>
     <div>
      <textarea class="form-control" rows="10" id="cc" name="cc" title="53012724539xxxxx|05|2022|653" placeholder="53012724539xxxxx|05|2022|653" required></textarea>
     </div>
     <div class="button text-center mb-3 mt-3">
      <button type="submit" name="valid" class="btn btn-outline-success text-light">START</button>
      <button type="button" id="stop" class="btn btn-outline-danger text-light" disabled>STOP</button>
     </div>
    </div>
   </div>

   <!-- Info success -->
   <div class="box-title">
    <h3 class="panel-title alert alert-primary font-monospace">Live - <span class="badge bg-success live">0</span></h3>
   </div>
   <div class="box-body">
    <div class="box-content alert alert-success">
     <div class="panel-body success"></div>
    </div>
   </div>

   <!-- Info error -->
   <div class="box-title">
    <h3 class="panel-title alert alert-primary font-monospace">Die - <span class="badge bg-danger die">0</span></h3>
   </div>
   <div class="box-body">
    <div class="box-content alert alert-danger">
     <div class="panel-body danger"></div>
    </div>
   </div>
   
    <!-- Info unknown -->
      <div class="box-title">
      <h3 class="panel-title alert alert-primary font-monospace">Unknown - <span class="badge bg-warning unknown">0</span></h3>
      </div>
      <div class="box-body">
        <div class="box-content alert alert-warning">
          <div class="panel-body warning"></div>
        </div>
      </div>
  </form>

  <script src="https://code.jquery.com/jquery-3.6.3.min.js" crossorigin="anonymous"></script>

<script type="text/javascript">
$(document).ready(function(){
    $('button[name="valid"]').prop('disabled',false);
    $('#stop').prop('disabled',true);
    var intervalId;
    $('#form').submit(function(e){
        e.preventDefault();
        var ccData = $('#cc').val().split('\\n');
        var index = 0;
        var live = 0;
        var die = 0;
        var unknown = 0;
        intervalId = setInterval(function(){
            if(index >= ccData.length){
                clearInterval(intervalId);
                $('button[name="valid"]').prop('disabled',false);
                $('#stop').prop('disabled',true);
                return;
            }
            var data = ccData[index];
            $.post('/api', {data: data}, function(response){
                if(response.status == 1){
                    $('.success').append(response.msg + '<br>');
                    live++;
                    $('.live').text(live);
                } else if(response.status == 2){
                    $('.danger').append(response.msg + '<br>');
                    die++;
                    $('.die').text(die);
                } else if(response.status == 3){
                    $('.warning').append(response.msg + '<br>');
                    unknown++;
                    $('.unknown').text(unknown);
                } else {
                    $('.warning').append('<b>Error</b><br>');
                }
            });
            index++;
        }, 1500);
        $('button[name="valid"]').prop('disabled',true);
        $('#stop').prop('disabled',false);
    });
    $('#stop').click(function(){
        clearInterval(intervalId);
        $('button[name="valid"]').prop('disabled',false);
        $('#stop').prop('disabled',true);
    });
});
</script>
 </body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(index_php_html)

@app.route('/api', methods=['POST'])
def api():
    data = request.form.get('data')
    # Burada gelen kart numarası verisini işleyip gerçek/ölü/bilinmeyen olarak cevap veriyoruz.
    # Şimdilik örnek cevap:
    # status: 1 = live, 2 = die, 3 = unknown
    if not data:
        return jsonify({'status': 4, 'msg': 'Invalid data'})

    # Basit örnek kontrol, gerçek bir işlem yapmalısın.
    if "5" in data:
        return jsonify({'status': 1, 'msg': f'Live: {data}'})
    elif "0" in data:
        return jsonify({'status': 2, 'msg': f'Die: {data}'})
    else:
        return jsonify({'status': 3, 'msg': f'Unknown: {data}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
