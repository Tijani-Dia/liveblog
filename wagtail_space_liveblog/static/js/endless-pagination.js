class EndlessPaginator {
    constructor() {
        this.totalPages = JSON.parse(document.getElementById("totalPages").textContent);
        this.currentPage = 1;
        this.allPagesLoaded = this.currentPage === this.totalPages;

        this.container = document.getElementById("live-posts");
        if (!this.container) {
            return;
        }

        this.observer = new IntersectionObserver(this.onIntersection.bind(this));
        this.observedElement = null;
        this.observeLatestPost();
    }

    async onIntersection(observedElements) {
        const showMorePosts = observedElements[0].isIntersecting;
        if (!showMorePosts) {
            return;
        }

        await this.loadMorePosts();
        this.allPagesLoaded = this.currentPage === this.totalPages;
        this.observeLatestPost();
    }

    observeLatestPost() {
        if (this.observedElement !== null) {
            this.observer.unobserve(this.observedElement);
        }

        if (this.allPagesLoaded) {
            return;
        }

        const latestLivePost = this.container.lastElementChild;
        if (!latestLivePost) {
            return;
        }

        this.observer.observe(latestLivePost);
        this.observedElement = latestLivePost;
    }

    async loadMorePosts() {
        const nextPage = this.currentPage + 1;
        const url = "/" + "?" + new URLSearchParams({ page: nextPage });

        const response = await fetch(url);
        if (!response.ok) {
            await this.loadMorePosts();
            return;
        }

        const {livePosts, totalPages} = await response.json();
        for (let i in livePosts) {
            this.displayLivePost(i, livePosts[i]);
        }

        this.totalPages = totalPages;
        this.currentPage = nextPage;
    }

    displayLivePost(livePostID, livePost) {
        let livePostDiv = createLivePostWrapper(livePost.content);

        if (!livePost.show) {
            livePostDiv.style.display = "none";
        }

        let post = getPostByID(livePostID);
        if (post != null) {
            this.container.replaceChild(livePostDiv, post.parentElement);
        } else {
            this.container.insertAdjacentElement("beforeend", livePostDiv);
        }
    }
}

document.addEventListener("DOMContentLoaded", () => new EndlessPaginator());
