$(document).ready(() => {
  showBucket();
});

// Toast notifikasi
const toastContent = $('.toast');
const toastMsg = $('#toast-msg');
const toast = new bootstrap.Toast(toastContent);

// Fungsi menampilkan semua wishlist
function showBucket() {

  const bucketList = $('#bucket-list');
  bucketList.html('<p>Loading...</p>');

  $.ajax({
    type: "GET",
    url: "/bucket",
    data: {},
    success: (response) => {
      bucketList.empty();
      const wishlists = response["wishlists"];
      if (wishlists.length) {
        wishlists.forEach(wishlist => {

          const wish = wishlist.wish;
          const done = wishlist.done;
          const num = wishlist.num;

          let temp_html = '';
          if (!done) {
            temp_html = `<li>
                          <h2>${wish}</h2>
                          <button onclick="doneBucket(${num})" id="done-btn" type="button" class="btn btn-outline-primary">Done!</button>
                          <button onclick="deleteBucket(${num})" type="button" class="btn btn-outline-danger">🗑️</button>
                        </li>`
          } else {
            temp_html = `<li>
                          <h2 class="done">${wish}</h2>
                          <button onclick="deleteBucket(${num})" type="button" class="btn btn-outline-danger">🗑️</button>
                        </li>`
          }
          bucketList.append(temp_html);
        });

      } else {
        bucketList.html("<p>Gada wishlist, cuyy. Ayolahh tambahin</p>");
      }
    }
  })
}

// Fungsi menambahkan wish ke list
function postBucket() {

  const bucket = $('#bucket').val();
  const form = document.forms['bucket-form'];
  const loadBtn = $('#loading-save');
  const saveBtn = $('#save-btn');

  // Handle input yang kosonggg
  if (!bucket) {
    alert("Please input your wish!");
    return
  }

  loadBtn.show();
  saveBtn.hide();
  $.ajax({
    type: "POST",
    url: "/bucket",
    data: { bucket },
    success: (response) => {
      toastMsg.html(`<strong>Naisseee!</strong> ${response.msg}`);
      toast.show();
      loadBtn.hide();
      saveBtn.show();
      form.reset();
      // jalanin fungi showBucket() biar ga perluu reload window
      showBucket();
    }
  })
}

// Fungsii wishlist kelarr
function doneBucket(num) {

  $.ajax({
    type: "POST",
    url: "/bucket/done",
    data: { num: num },
    success: (response) => {
      toastMsg.html(`<strong>Yeayyyy!</strong> ${response.msg}`);
      toast.show();
      // jalanin fungi showBucket() biar ga perluu reload window
      showBucket();
    }
  })
}

// Fungsi menghapus wish
function deleteBucket(num) {
  const isDelete = confirm("Are you sure, wanna delete this wish?");

  if (isDelete) {
    $.ajax({
      type: "POST",
      url: "/delete",
      data: { num: num },
      success: (response) => {
        toastMsg.html(`<strong>Thanks!</strong> ${response.msg}`);
        toast.show();
        // jalanin fungi showBucket() biar ga perluu reload window
        showBucket();
      }
    })
  }
}