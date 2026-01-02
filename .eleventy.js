const nunjucks = require("nunjucks");
const crypto = require("crypto");

// Generate a hash for this build
const buildHash = crypto.createHash('md5').update(Date.now().toString()).digest('hex').substring(0, 8);

module.exports = function (eleventyConfig) {
  eleventyConfig.addPassthroughCopy({ "src/static": "/" });

  eleventyConfig.addNunjucksFilter("json", (value) => {
    const json = value === undefined ? "null" : JSON.stringify(value);
    return new nunjucks.runtime.SafeString(json);
  });

  eleventyConfig.addFilter("jsonString", (value) => {
    return value === undefined ? "null" : JSON.stringify(value);
  });

  eleventyConfig.addFilter("stripHtml", (value) => {
    const str = typeof value === "string" ? value : "";
    return str.replace(/<[^>]*>/g, " ").replace(/\s+/g, " ").trim();
  });

  eleventyConfig.addFilter("truncate", (value, maxLength = 180) => {
    const str = typeof value === "string" ? value : "";
    if (str.length <= maxLength) return str;
    return str.slice(0, Math.max(0, maxLength - 1)).trimEnd() + "…";
  });

  eleventyConfig.addFilter("extractFirstUrl", (value) => {
    const str = typeof value === "string" ? value : "";
    const match = str.match(/https?:\/\/[^\s"'<>]+/i);
    return match ? match[0] : null;
  });

  eleventyConfig.addFilter("unescape", (value) => {
    const str = typeof value === "string" ? value : "";
    return str.replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#39;/g, "'");
  });

  eleventyConfig.addFilter("toRfc822", (value) => {
    const date = value instanceof Date ? value : new Date(value);
    if (Number.isNaN(date.getTime())) return "";
    return date.toUTCString();
  });

  eleventyConfig.addFilter("cacheBust", (url) => {
    return `${url}?v=${buildHash}`;
  });

  eleventyConfig.addCollection("organizations", (collectionApi) => {
    return collectionApi.getFilteredByGlob("./src/content/organizations/**/*.md");
  });

  eleventyConfig.addCollection("feed", (collectionApi) => {
    const items = collectionApi.getFilteredByGlob("./src/content/organizations/**/*.md");
    return items.slice().sort((a, b) => (b.date || 0) - (a.date || 0)).slice(0, 50);
  });

  return {
    dir: {
      input: "src",
      includes: "_includes",
      data: "_data",
      output: "_site"
    },
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
    templateFormats: ["njk", "md", "html"]
  };
};
