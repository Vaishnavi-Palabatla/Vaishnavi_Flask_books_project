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
    text=text+"<th scope='row'><a href='{{ url_for('id',id=book.id) }}' method='GET' id = '{{ book.id  }}' >"+books_display[book].isbn+"</th>"
    text=text+"<td>"+books_display[book].Title+"</td>"
    text=text+"<td>"+books_display[book].Author+"</td>"
    text=text+"<td>"+books_display[book].Year+"</td>"
    text=text+"</tr>"
    }
    
    console.log(text)
    document.getElementsByTagName("tbody")[0].innerHTML=text})
    .catch(error => console.log('error', error));
}

