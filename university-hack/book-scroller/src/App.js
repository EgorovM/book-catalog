import React from 'react';
import {Grid} from "./grid/Grid";
import {apiRequest} from "./utils";
import './static/common.scss';

export default class App extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            loading: true,
            screenWidth: window.innerWidth,
            allBooks: [],
            categorizedBooks: {}
        }
    }

    componentDidMount() {
        window.onresize = () => {
            this.setState({screenWidth: window.innerWidth})
        };
        window.onscroll = () => {
            const {loading} = this.state;
            if ((window.innerHeight + window.pageYOffset) >= document.body.offsetHeight - 2 && !loading) {
                this.loadBooks()
            }
        };
        apiRequest(({books}) => {
            this.setState({allBooks: [...this.state.allBooks, ...books], loading: false})
        }, 'load_books', {data: {books: {}}, method: "POST"})
    }

    categorize(bookId, category) {
        const {
            allBooks,
            categorizedBooks
        } = this.state;
        const book = allBooks.find(b => b.id === bookId);
        const newCategory = book.category === category ? '' : category;
        book.category = newCategory;
        this.setState({
            allBooks: allBooks,
            categorizedBooks: {...categorizedBooks, [bookId]: newCategory}
        })
    }

    loadBooks() {
        const {categorizedBooks, allBooks} = this.state;
        this.setState({loading: true});
        apiRequest(({books}) => {
            this.setState({allBooks: [...allBooks, ...books], loading: false})
        }, 'load_books', {data: {books: categorizedBooks}, method: "POST"})
    }

    render() {
        return (
            <div>
                <Grid categorize={this.categorize.bind(this)} {...this.state}/>
            </div>
        )
    }
}
