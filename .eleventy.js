module.exports = function (eleventyConfig) {
  eleventyConfig.addPassthroughCopy({ "src/assets": "assets" });
  eleventyConfig.addPassthroughCopy({ "src/CNAME": "CNAME" });

  eleventyConfig.addFilter("limit", function (array, count) {
    return Array.isArray(array) ? array.slice(0, count) : [];
  });

  eleventyConfig.addFilter("where", function (array, key, value) {
    return Array.isArray(array) ? array.filter((item) => item[key] === value) : [];
  });

  eleventyConfig.addFilter("dateDisplay", function (date) {
    return new Intl.DateTimeFormat("en-US", {
      month: "long",
      day: "numeric",
      year: "numeric"
    }).format(new Date(date));
  });

  eleventyConfig.addCollection("posts", function (collectionApi) {
    return collectionApi.getFilteredByGlob("./src/blog/*.md").sort((a, b) => {
      return b.date - a.date;
    });
  });

  eleventyConfig.addCollection("maps", function (collectionApi) {
    return collectionApi.getFilteredByGlob("./src/maps/*.md").sort((a, b) => {
      return b.date - a.date;
    });
  });

  eleventyConfig.addCollection("parks", function (collectionApi) {
    const maps = collectionApi.getFilteredByGlob("./src/maps/*.md");
    const parksData = require("./src/_data/parks-base.js");
    return parksData.map(park => {
      const count = maps.filter(map => map.data.parkSlug === park.slug).length;
      return {
        ...park,
        count
      };
    });
  });

  eleventyConfig.addCollection("years", function (collectionApi) {
    const maps = collectionApi.getFilteredByGlob("./src/maps/*.md");
    const decades = ["1980s", "1990s", "2000s", "2010s", "2020s"];
    return decades.map(decade => {
      const count = maps.filter(map => map.data.decade === decade).length;
      return {
        decade,
        count,
        url: `/years/#${decade}`
      };
    });
  });

  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      data: "_data"
    },
    htmlTemplateEngine: "njk",
    markdownTemplateEngine: "njk"
  };
};
