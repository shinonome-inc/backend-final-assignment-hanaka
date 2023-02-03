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

const changeLike = async (id) => {
    // buttonのid ( = "tweet-{{tweet.id}}" )
    const like_button = document.querySelector("#" + id)
    const url = like_button.dataset.url;
    const data = {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": csrftoken,
        }
    };
    const response = await fetch(url, data);
    const tweet_data = await response.json();
    changeStyle(tweet_data, like_button);
}

const changeStyle = (tweet_data, like_button) => {
    const like_count = document.querySelector(".count_" + tweet_data.tweet_id)

    if (tweet_data.is_liked) {
        unlike_url = tweet_data.unlike_url;
        like_button.setAttribute("data-url", unlike_url);
        like_button.innerHTML = '<i class="fa-solid fa-heart fa-lg" style="color:red;"></i>';
        like_count.textContent = tweet_data.like_count;
    } else {
        like_url = tweet_data.like_url;
        like_button.setAttribute("data-url", like_url);
        like_button.innerHTML = '<i class="fa-regular fa-heart fa-lg"></i>';
        like_count.textContent = tweet_data.like_count;

    }

}
