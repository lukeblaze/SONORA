import React, { useState } from 'react';
import axios from 'axios';

const EmotionInput = () => {
    const [features, setFeatures] = useState({ feature1: '', feature2: '' });
    const [recommendations, setRecommendations] = useState(null);
    const [error, setError] = useState('');

    // Handle form input change
    const handleChange = (e) => {
        setFeatures({
            ...features,
            [e.target.name]: e.target.value
        });
    };

    // Handle form submission
    const handleSubmit = async (e) => {
        e.preventDefault();

        // Send POST request to the Django backend
        try {
            const response = await axios.post('http://127.0.0.1:8000/emotion/recommendations/', {
                features: [features.feature1, features.feature2]
            });

            // Set the recommended songs
            setRecommendations(response.data.songs);
            setError('');
        } catch (err) {
            setError('Failed to fetch recommendations.');
            setRecommendations(null);
        }
    };

    return (
        <div className="container">
            <h2>Enter Features for Emotion Detection</h2>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="feature1">Feature 1</label>
                    <input
                        type="text"
                        className="form-control"
                        id="feature1"
                        name="feature1"
                        value={features.feature1}
                        onChange={handleChange}
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="feature2">Feature 2</label>
                    <input
                        type="text"
                        className="form-control"
                        id="feature2"
                        name="feature2"
                        value={features.feature2}
                        onChange={handleChange}
                    />
                </div>
                <button type="submit" className="btn btn-primary">Submit</button>
            </form>

            {error && <div className="alert alert-danger mt-3">{error}</div>}

            {recommendations && (
                <div className="mt-3">
                    <h3>Recommended Songs for Emotion</h3>
                    <ul>
                        {recommendations.map((song, index) => (
                            <li key={index}>{song.song_name} by {song.artist}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default EmotionInput;
