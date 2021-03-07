// ES6 module syntax
import polka from 'polka';
import mock_costumers from "../db/mock_data_costumers.json";
import mock_books from "../db/mock_data_books.json";

// Utils class is used to help hidrate forms
class Utils {
    get_mock(req, res, next) {
        var tipo = req.params.tipo;
        var mock = [];
        if (tipo == "costumer")
            mock = mock_costumers
        else if (tipo == "book")
            mock = mock_books

        res.setHeader('Content-Type', 'application/json');
        res.end(JSON.stringify(mock));
    }

    routes = polka()
        .get("/mock/:tipo", this.get_mock);
}

const utils = new Utils();

export default utils.routes;