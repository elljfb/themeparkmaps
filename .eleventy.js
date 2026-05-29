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
