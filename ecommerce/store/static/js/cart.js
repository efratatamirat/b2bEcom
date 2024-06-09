var updateBtns = document.getElementsByClassName('update-cart')
/*
for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('productId:', productId, 'Action:', action)
        console.log('USER:', user)

		if (user == 'AnonymousUser'){
			updateUserOrder('User is not authenticated')
		}else{
			updateUserOrder(productId, action)
		}
	})
}
*/
/*The code above was the code from the video of making the store and everything else
and the code bellow was the code from AI that i corected because i needed to defin the csrf token in the 
code as well, you can see it in line 31*/ 
for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
      var productId = this.dataset.product;
      var action = this.dataset.action;
      console.log('productId:', productId, 'Action:', action);
      console.log('USER:', user);
  
      if (user == 'AnonymousUser') {
        addCookieItem(productId, action)
      } else {
        var csrftoken = getToken('csrftoken'); // Retrieve the CSRF token
        updateUserOrder(productId, action, csrftoken);
      }
    });
  }

  function addCookieItem(productId, action){
    console.log('User is not authenticated')
  
    if (action == 'add'){
      if (cart[productId] == undefined){
      cart[productId] = {'quantity':1}
  
      }else{
        cart[productId]['quantity'] += 1
      }
    }
  
    if (action == 'remove'){
      cart[productId]['quantity'] -= 1
  
      if (cart[productId]['quantity'] <= 0){
        console.log('Item should be deleted')
        delete cart[productId];
      }
    }
    console.log('CART:', cart)
    document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
    
    location.reload()
  }
  
/*  
function updateUserOrder(productId, action){
    console.log('User is authenticated, sending data... ')

    var url = '/update_item/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        }, 
        body:JSON.stringify({'productId':productId, 'action':action})
    })
    .then((response) => {
       return response.json();
    })
    .then((data) => {
       console.log('data:', data)
    });
}
*/
/*The code above was the code from the video of making the store and everything else
and the code bellow was the code from AI that i corected because i needed to defin the csrf token in the code as well 
you can see it in line 71
function updateUserOrder(productId, action, csrftoken) {
    console.log('User is authenticated, sending data... ');
  
    var url = '/update_item/';
  
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({ 'productId': productId, 'action': action })
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        console.log('data:', data);
        location.reload()
      });
  }
*/

function updateUserOrder(productId, action, csrftoken) {
  if (user === 'AnonymousUser') {
    console.log('User is not logged in');
    // Perform any necessary actions when the user is not authenticated
  } else {
    console.log('User is authenticated, sending data...');

    var url = '/update_item/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'productId': productId,
            'action': action,
            'quantity': 100 // Set the quantity to 100

          })
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log('data:', data);
        location.reload();
    });
  }
}

