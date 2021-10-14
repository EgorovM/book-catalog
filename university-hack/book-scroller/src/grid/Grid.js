import React from "react";
import './styles.scss';
import {Book} from "./book/Book";
import {InfoBox} from "./info-box/InfoBox";
import {Loading} from "./loading/Loading";
import {getParents} from "../utils";

export class Grid extends React.Component {
    constructor(props) {
        super(props);

        let columnsNumber = 4;
        const {screenWidth} = props;
        if (screenWidth <= 1280) {
            columnsNumber = 3
        }
        if (screenWidth <= 960) {
            columnsNumber = 2
        }
        if (screenWidth <= 640) {
            columnsNumber = 1
        }
        this.state = {
            popup: false,
            columnsNumber: columnsNumber
        };

        this.popupForm = React.createRef();
    }

    componentDidUpdate(prevProps, prevState, _) {
        let columnsNumber = 4;
        const {screenWidth} = prevProps;
        if (screenWidth <= 1280) {
            columnsNumber = 3
        }
        if (screenWidth <= 960) {
            columnsNumber = 2
        }
        if (screenWidth <= 640) {
            columnsNumber = 1
        }
        if (columnsNumber !== prevState.columnsNumber) {
            this.setState({
                columnsNumber: columnsNumber
            })
        }
    }

    componentDidMount() {
        window.onmousedown = e => {
            if (!getParents(e.target).includes(this.popupForm.current) && this.state.popup) {
                this.togglePopup();
            }
        }
    }

    togglePopup(book = false) {
        this.setState({popup: !this.state.popup ? book : false})
    }

    render() {
        const {
            columnsNumber,
            popup
        } = this.state;
        const sizes = {
            4: 256,
            3: 245,
            2: 224,
            1: 0
        };
        const {
            allBooks,
            categorize,
            loading
        } = this.props;
        let columns = [...Array(columnsNumber).keys()].map(() => ({overallHeight: 0, books: []}));
        allBooks.forEach((book) => {
            let {image_height, image_width} = book;
            image_height = Math.ceil(image_height * sizes[columnsNumber] / image_width);
            let minHeight = Math.min(...columns.map(c => c.overallHeight));
            const col = columns.find(c => (c.overallHeight === minHeight));
            col.books.push(book);
            col.overallHeight += image_height;
        });
        return (
            <>
                {popup && <InfoBox popupForm={this.popupForm} categorize={categorize} {...popup} toggle={this.togglePopup.bind(this)} />}
                <div className={`grid${popup ? ' blurred' : ''}`}>
                    {columns.map(({books}, index) => (
                        <div key={index} className="col">
                            {books.map((book, index) => (
                                <Book key={index} categorize={categorize} book={book} onClick={this.togglePopup.bind(this)}/>
                            ))}
                        </div>
                    ))}
                </div>
                {loading && <Loading/>}
            </>
        );
    }
}
