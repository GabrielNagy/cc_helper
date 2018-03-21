function(req, res) {
    provides("json", function() {
        var results = [];
        var returnedGenres = [];
        var genres_to_search = ["biography", "fantasy", "horror", "animation", "adventure", "comedy", "action", "thriller", "crime", "drama", "mystery", "sci-fi", "romance"];
        var ratings_to_search = ["ag", "ap-12", "n-15", "im-18"];
        var imax, fourdx, technology, subbedOrDubbed, returnedRating;
        while(row = getRow()) {
            returnedGenres = [];
            returnedRating = '';
            imax = false;
            fourdx = false;
            if (row.key[3].indexOf("2d") != -1) {
                technology = "2d";
            } else if(row.key[3].indexOf("3d") != -1) {
                technology = "3d";
            }
            if (row.key[3].indexOf("imax") != -1) {
                imax = true;
            }
            if (row.key[3].indexOf("4dx") != -1) {
                fourdx = true;
            }
            if (row.key[3].indexOf("dubbed") != -1) {
                dubbed = true;
            } else dubbed = false;

            genres_to_search.forEach(function(genre) {
                if (row.key[3].indexOf(genre) != -1) {
                    returnedGenres.push(genre);
                }
            });

            ratings_to_search.forEach(function(rating) {
                if (row.key[3].indexOf(rating) != -1) {
                    returnedRating = rating;
                }
            });

            results.push({
                date: row.key[0],
                title: row.key[1],
                link: row.key[2],
                tech: technology,
                isImax: imax,
                is4dx: fourdx,
                dubbed: dubbed,
                length: row.key[4],
                releaseYear: row.key[5],
                genres: returnedGenres,
                hour: row.value,
                rating: returnedRating
            });
        }
        send(JSON.stringify(results));
    });
}
