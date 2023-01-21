const getCookie = (name) => {
    if (document.cookie && document.cookie !== '') {
        for (const cookie of document.cookie.split(';')) {
            const [key, value] = cookie.trim().split('=')
            if (key === name) {
                return decodeURIComponent(value)
            }
        }
    }
}
const csrftoken = getCookie('csrftoken')

async function changeLike() {
    const like_button = document.querySelector("#like_button")
    const url = like_button.dataset.url;
    const data = {
        method: "POST",
        Headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": csrftoken,
        }
    };
    const response = await fetch(url, data);
    const tweet_data = await response.json();
    changeStyle(tweet_data, like_button);
}

const changeStyle = (tweet_data, like_button) => {
    if (tweet_data.is_liked) {
        unlike_url = tweet_data.url
        like_button.setAttribute("unlike_url", unlike_url);
        like_button.innerHTML = '<i class="fa-solid fa-heart fa-lg" style="color:red;"></i>';
    } else {
        like_url = tweet_data.url
        like_button.setAttribute("like_url", like_url);
        like_button.innerHTML = '<i class="fa-regular fa-heart fa-lg"></i>';
    }

}
