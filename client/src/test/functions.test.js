import { assert } from 'chai';
import fetch from 'node-fetch';

/*
    TO RUN:
    Add
    
    "type": "module",

    to package.json
*/

describe('Test functions', () => {
    it('Convex hull', () => {
        const data = {
            table: 'nyc_subway_stations'
        };
          
        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        };

        assert.doesNotThrow(() => {
            fetch('convex', options)
            .then(res => res.json())
            .then(json => assert.equal(json.body.coordinates[0][0], [563292.1172580556, 4484900.921251608]))
        });
    }).timeout(5000);

    it('Count points in polygon', () => {
        const data = {
            polygon: 1,
            points: 'nyc_subway_stations',
            sub_table: 'nyc_polygon'
        };

        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        };

        assert.doesNotThrow(() => {
            fetch('/count', options)
            .then(res => res.json())
            .then(json => assert.equal(json.body, 491));
        });
    }).timeout(5000);

    it('Voronoi polygon', () => {
        const data = {
            table: 'nyc_subway_stations'
        };

        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        };

        assert.doesNotThrow(() => {
            fetch('/voronoi', options)
            .then(res => res.json())
            .then(json => { console.log(json.body); assert.isNotEmpty(json.body)});
        });

    }).timeout(10000);
});

// ..
