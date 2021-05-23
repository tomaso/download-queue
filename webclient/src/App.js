import React, { Component } from "react";
import Modal from "./components/Modal";
import axios from "axios";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      viewCompleted: false,
      downloadJobList: [],
      queueList: [],
      modal: false,
      activeItem: {
        target_directory: "",
        target_file: "",
        url: "",
        queue: null,
        completed: false,
        priority: 0,
        progress: 0,
      },
    };
  }

  componentDidMount() {
    this.refreshList();
    setInterval(this.refreshList, 2000);
  }

  refreshList = () => {
    console.debug("Refreshing list")
    axios
      .get("http://localhost:8000/api/download_jobs/")
      .then((res) => this.setState({ downloadJobList: res.data }))
      .catch((err) => console.log(err));
    axios
      .get("http://localhost:8000/api/queues/")
      .then((res) => this.setState({ queueList: res.data }))
      .catch((err) => console.log(err));    
  };

  toggle = () => {
    this.setState({ modal: !this.state.modal });
  };

  handleSubmit = (item) => {
    this.toggle();

    if (item.id) {
      axios
        .put(`http://localhost:8000/api/download_jobs/${item.id}/`, item)
        .then((res) => this.refreshList());
      return;
    }
    axios
      .post("http://localhost:8000/api/download_jobs/", item)
      .then((res) => this.refreshList());  
  };

  handleDelete = (item) => {
    axios
      .delete(`http://localhost:8000/api/download_jobs/${item.id}/`)
      .then((res) => this.refreshList());
  };

  createItem = () => {
    const item = { target_directory: "", target_file: "", url: "", queue: 1, completed: false, priority: 0, progress: 0};

    this.setState({ activeItem: item, modal: !this.state.modal });
  };

  editItem = (item) => {
    this.setState({ activeItem: item, modal: !this.state.modal });
  };

  displayCompleted = (status) => {
    if (status) {
      return this.setState({ viewCompleted: true });
    }

    return this.setState({ viewCompleted: false });
  };

  renderTabList = () => {
    return (
      <div className="nav nav-tabs">
        <span
          className={this.state.viewCompleted ? "nav-link active" : "nav-link"}
          onClick={() => this.displayCompleted(true)}
        >
          Complete
        </span>
        <span
          className={this.state.viewCompleted ? "nav-link" : "nav-link active"}
          onClick={() => this.displayCompleted(false)}
        >
          Incomplete
        </span>
      </div>
    );
  };

  renderItems = () => {
    const { viewCompleted } = this.state;
    const newItems = this.state.downloadJobList.filter(
      (item) => item.completed === viewCompleted
    );

    return newItems.map((item) => (
      <tr
        key={item.id}
      >
        <td
          className={`todo-title mr-2 ${
            this.state.viewCompleted ? "completed-todo" : ""
          }`}
          title={item.url}
        >
          {item.url}
        </td>
        <td>
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-arrow-right" viewBox="0 0 16 16">
            <path fillRule="evenodd" d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8z"/>
          </svg>
        </td>
        <td
          title={item.target_directory}
        >
          {item.target_directory}{item.target_file}
        </td>
        <td>
          <div class="progress">
            <div class="progress-bar" role="progressbar" style={{width: item.progress + '%'}}  aria-valuemin="0" aria-valuemax="100">{item.progress}%</div>
          </div>
        </td>
        <td>
          <button
            className="btn btn-secondary mr-2"
            onClick={() => this.editItem(item)}
          >
            Edit
          </button>
          <button
            className="btn btn-danger"
            onClick={() => this.handleDelete(item)}
          >
            Delete
          </button>
        </td>
      </tr>
    ));
  };

  render() {
    return (
      <main className="container">
        <h1 className="text-white text-uppercase text-center my-4">Download queue</h1>
        <div className="row">
          <div className="col-md-12 col-sm-10 mx-auto p-0">
              <div className="mb-4">
                <button
                  className="btn btn-primary"
                  onClick={this.createItem}
                >
                  Add download job
                </button>
              </div>
              {this.renderTabList()}
              <table class="table">
                <thead>
                  <tr>
                    <th scope="col">URL</th>
                    <th scope="col"></th>
                    <th scope="col">Target</th>
                    <th scope="col">Progress</th>
                    <th scope="col">Operations</th>
                  </tr>
                </thead>
                <tbody>
                  {this.renderItems()}
                </tbody>
              </table>
            
          </div>
        </div>
        {this.state.modal ? (
          <Modal
            activeItem={this.state.activeItem}
            queueList={this.state.queueList}
            toggle={this.toggle}
            onSave={this.handleSubmit}
          />
        ) : null}
      </main>
    );
  }
}

export default App;