import { assert } from 'chai';
import fetch from 'node-fetch';

describe('Test router', () => {
    it('Postgres connection', done => {
        const options = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        };

        fetch('http://localhost:5000/', options)
        .then(res => res.json())
        .then(json => { 
            assert.isTrue(json.body);
            done();
        })
        .catch(err => {
            done(err);
        });
    });
});