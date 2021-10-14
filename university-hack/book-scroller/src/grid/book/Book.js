import React from "react";
import './styles.scss';
import likeSVG from './media/like.svg';
import dislikeSVG from './media/dislike.svg';
import {getParents} from "../../utils";

export class Book extends React.Component {

    render() {
        const {
            book,
            onClick,
            categorize
        } = this.props;
        const {
            id,
            name,
            image_link,
            category
        } = book;
        return (
            <div onClick={e => {
                Array.from(document.getElementsByClassName('book'))
                    .forEach(item => {item.classList.remove('active')});
                getParents(e.target)[1].classList.toggle('active')
            }} className={`book${category !== '' ? ` categorized ${category}`: ''}`}>
                <img className="cover" src={image_link} alt="book"/>
                {category === 'interested' && <div className="categorized liked">
                    <img src={likeSVG} alt="interested in"/>
                </div>}
                {category === 'not_interested' && <div className="categorized disliked">
                    <img src={dislikeSVG} alt="not interested in"/>
                </div>}
                <div className="options">
                    <button onClick={() => {
                        categorize(id, 'interested')
                    }} className="like">
                        <div className={`img-box${category === 'interested' ? ' active' : ''}`}>
                            <img src={likeSVG} alt="interested in"/>
                        </div>
                    </button>
                    <button onClick={() => {
                        onClick(book)
                    }} className="info">
                        <div className="info-box">
                            <div className="name">
                                {name.split(' ').slice(0, 3).join(' ')}{name.split(' ').length > 3 ? '...' : ''}
                            </div>
                        </div>
                    </button>
                    <button onClick={() => {
                        categorize(id, 'not_interested')
                    }} className="dislike">
                        <div className={`img-box${category === 'not_interested' ? ' active' : ''}`}>
                            <img src={dislikeSVG} alt="not interested in"/>
                        </div>
                    </button>
                </div>
            </div>
        );
    }
}