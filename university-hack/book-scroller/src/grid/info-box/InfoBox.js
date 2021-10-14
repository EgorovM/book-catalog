import React from "react";
import './styles.scss';
import crossSVG from './media/cross.svg';
import likeSVG from './media/like.svg';
import dislikeSVG from './media/dislike.svg';

export class InfoBox extends React.Component {
    render() {
        const {
            popupForm,
            toggle,
            id,
            name,
            author,
            description,
            labels,
            category,
            categorize
        } = this.props;
        return (
            <div className="info-popup">
                <div ref={popupForm} className="form">
                    <span onClick={toggle} className="close">
                        <img src={crossSVG} alt="close"/>
                    </span>
                    <div className="name">{name}</div>
                    <div className="author">{author}</div>
                    <div className="labels">
                        {labels.split(';').slice(0, labels.split(';').length - 1).map((item, index) => (
                            <div key={index} className="label">
                                {item}
                            </div>
                        ))}
                    </div>
                    <div className="description">{description}</div>
                    <div className="buttons">
                        <img onClick={() => {
                            categorize(id, 'interested')
                        }} className={`like${category === 'interested' ? ' active' : ''}`} src={likeSVG}
                             alt="interested in"/>
                        <img onClick={() => {
                            categorize(id, 'not_interested')
                        }} className={`dislike${category === 'not_interested' ? ' active' : ''}`} src={dislikeSVG}
                             alt="not interested in"/>
                    </div>
                </div>
            </div>
        );
    }
}