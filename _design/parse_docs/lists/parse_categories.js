function(req, res) {
    function dynamicSort(property) {
        return function (obj1,obj2) {
            return obj1[property] > obj2[property] ? 1
                : obj1[property] < obj2[property] ? -1 : 0;
        }
    }
    function dynamicSortMultiple() {
        var props = arguments;
        return function (obj1, obj2) {
            var i = 0, result = 0, numberOfProperties = props.length;
            while(result === 0 && i < numberOfProperties) {
                result = dynamicSort(props[i])(obj1, obj2);
                i++;
            }
            return result;
        }
    }
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
            if (row.key[4].indexOf("2d") != -1) {
                technology = "2d";
            } else if(row.key[4].indexOf("3d") != -1) {
                technology = "3d";
            }
            if (row.key[4].indexOf("imax") != -1) {
                imax = true;
            }
            if (row.key[4].indexOf("4dx") != -1) {
                fourdx = true;
            }
            if (row.key[4].indexOf("dubbed") != -1) {
                dubbed = true;
            } else dubbed = false;

            genres_to_search.forEach(function(genre) {
                if (row.key[4].indexOf(genre) != -1) {
                    returnedGenres.push(genre);
                }
            });

            ratings_to_search.forEach(function(rating) {
                if (row.key[4].indexOf(rating) != -1) {
                    returnedRating = rating;
                }
            });

            results.push({
                date: row.key[0],
                title: row.key[2],
                link: row.key[3],
                tech: technology,
                isImax: imax,
                is4dx: fourdx,
                dubbed: dubbed,
                length: row.key[5],
                releaseYear: row.key[6],
                genres: returnedGenres,
                hour: row.value,
                rating: returnedRating
            });
        }
        var sorted = results.sort(dynamicSortMultiple("title", "tech", "isImax", "is4dx"));
        send(JSON.stringify(results));
    });
}
