function searchbook(event){
    var x=document.forms["search"]["books"].value;
    var y=document.forms["search"]["searchname"].value;
    console.log(x)
    console.log(y)

    var formdata = new FormData();
    formdata.append("books", x);
    formdata.append("searchname", y);

    var requestOptions = {
    method: 'POST',
    body: formdata,
    redirect: 'follow'
    };

    fetch("/books", requestOptions)
    .then(response => response.text())
    .then((result)=> {console.log(result)
    books_display=JSON.parse(result)
    let text=""
    for (let book in books_display){
    // console.log(books_display[book])
    text=text+"<tr>"
    text=text+"<th scope='row'><a href='javascript:null' onClick='bookFunction(this.innerHTML)'>"+books_display[book].isbn+"</th>"
    text=text+"<td>"+books_display[book].Title+"</td>"
    text=text+"<td>"+books_display[book].Author+"</td>"
    text=text+"<td>"+books_display[book].Year+"</td>"
    text=text+"</tr>"
    }
    
    console.log(text)
    document.getElementsByTagName("tbody")[0].innerHTML=text})
    .catch(error => console.log('error', error));
}
function bookFunction(content){
    // location.replace("/details.html")
    var settings = {
        "url": "/review",
        "method": "GET",
        "timeout": 0,
      };
      
      $.ajax(settings).done(function (response) {
        // console.log(response);
        $("html").html(response)

      });

    // alert(content)
    var form = new FormData();
    // form.append("bookform_data", "the");

    var settings = {
    "url": "/id/"+content,
    "method": "GET",
    "timeout": 0,
    "headers": {
        "Cookie": "session=eyJib29raWQiOiIxODU3MjMxMDgyIn0.YQt-pg.aY6CvSptDuE97NDvmQh5C36Hexg"
    },
    "processData": false,
    "mimeType": "multipart/form-data",
    "contentType": false,
    "data": form
    };

    $.ajax(settings).done(function (response) {
    console.log(response);
    const dbParam = JSON.parse(response);
    let text = "<tbody>"
    for (let x in dbParam.bookdetais) {
        // console.log(dbParam[x])
        text+="<tr>"
        text += "<th scope='row'><a href='javascript: null' onclick='bookFunction(this.innerHTML)'>" + dbParam.bookdetais[x].isbn + "</a></th>";
        text+= "<td>"+dbParam.bookdetais[x].Title+"</td>"
        text+= "<td>"+dbParam.bookdetais[x].Author+"</td>"
        text+= "<td>"+dbParam.bookdetais[x].Year+"</td>"
        text+="</tr>"
    }  
    text+="</tbody>" 
    // console.log(text)
    document.getElementsByTagName("tbody")[0].innerHTML = text;

    let revhtml=" "
    for(let y in dbParam.reviews_dict){
        revhtml+='<blockquote class="blockquote">'
        revhtml+= '<footer class="blockquote-footer float-left">'+ dbParam.reviews_dict[y].email+ '</footer>'
        revhtml+= '<div class="float-right">'
            for(let rat in parseInt(dbParam.reviews_dict[y].rating)){
                console.log(rat)
            }
              
        revhtml+= '</div><br></br><p class="mb-0">'+dbParam.reviews_dict[y].review+'</p>'
          
        revhtml+='</blockquote><hr></hr>'
        
    }
    document.getElementById('rev').innerHTML = revhtml
    });
}
