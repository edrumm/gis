import { assert } from 'chai';
import fetch from 'node-fetch';

/*
    Change lockfile test command to /node_modules/../mocha instead of mocha ... ?
*/

describe('Test route', () => {
    it('Performs convex hull', () => {
        const data = {
            points: 'geom',
            table: 'nyc_subway_stations'
        };
          
        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        };
        
        fetch('/test', options)
        .then(res => res.json())
        .then(json => assert.isNotEmpty(json.body))
        .catch(err => assert.fail(err));
    });
});

// ..
