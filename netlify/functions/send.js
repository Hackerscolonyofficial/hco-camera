const fetch = require("node-fetch");

exports.handler = async (event) => {
    try {
        const response = await fetch("https://YOURUSERNAME.pythonanywhere.com/send", {
            method: "POST",
            headers: { "Content-Type": event.headers["content-type"] },
            body: event.body
        });
        return { statusCode: 200, body: "OK" };
    } catch (err) {
        return { statusCode: 500, body: "Error: " + err.message };
    }
};
