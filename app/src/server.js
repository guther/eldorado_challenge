// ES6 module syntax
import sirv from 'sirv';
import polka from 'polka';
import compression from 'compression';
import * as sapper from '@sapper/server';
import utils from './utils';

// CommonJS syntax (these modules do not support ES6 module syntax)
const bodyParser = require('body-parser');
const { PORT, NODE_ENV } = process.env;
const dev = NODE_ENV === 'development';

polka()
	.use(bodyParser.urlencoded({ extended: false }))
	.use(bodyParser.json())

	.use("/utils", utils)
	.use(
		compression({ threshold: 0 }),
		sirv('static', { dev }),
		sapper.middleware({
			session: (req, res) => ({
				posts: {}
			})
		})
	)
	.listen(PORT, err => {
		if (err) console.log('error', err);
	});