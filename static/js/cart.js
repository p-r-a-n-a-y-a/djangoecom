var cartBtns = document.getElementsByClassName('updateCart')


for(var i=0; i < cartBtns.length; i++){
    cartBtns[i].addEventListener('click',function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        if(user === 'AnonymousUser'){
            alert('login to buy')
            // updateUserOrder(productId,action)
        }else{
            updateUserOrder(productId,action)
        }
    })
}

function updateUserOrder(productId, action) {
    var url = "/update_items/"

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({'productId':productId,'action':action})
    })

    .then((response) =>{
        return response.json()
        // console.log(response)
    })

    .then((data) =>{
        console.log('data:',data)
        location.reload()
    })
}