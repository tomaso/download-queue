import React, { Component } from "react";
import {
  Button,
  Modal,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Form,
  FormGroup,
  Input,
  Label,
} from "reactstrap";

export default class CustomModal extends Component {
  constructor(props) {
    super(props);
    this.state = {
      activeItem: this.props.activeItem,
      queueList: this.props.queueList
    };
  }

  handleChange = (e) => {
    let { name, value } = e.target;

    if (e.target.type === "checkbox") {
      value = e.target.checked;
    }

    const activeItem = { ...this.state.activeItem, [name]: value };

    this.setState({ activeItem });
  };


  render() {
    const { toggle, onSave } = this.props;

    return (
      <Modal isOpen={true} toggle={toggle}>
        <ModalHeader toggle={toggle}>Todo Item</ModalHeader>
        <ModalBody>
          <Form>
            <FormGroup>
              <Label for="download_job-queue">Queue</Label>
              <Input
                type="select"
                id="download_job-target_file"
                name="queue"
                value={this.state.activeItem.queue}
                onChange={this.handleChange}
                placeholder="Queue">
              {this.state.queueList.map((e, key) => {
                return <option value={e.id}>{e.name}</option>;
              })}
              </Input>
            </FormGroup>
            <FormGroup>
              <Label for="download_job-url">URL</Label>
              <Input
                type="text"
                id="download_job-url"
                name="url"
                value={this.state.activeItem.url}
                onChange={this.handleChange}
                placeholder="URL to download"
              />
            </FormGroup>
            <FormGroup>
              <Label for="download_job-target_directory">Target directory</Label>
              <Input
                type="text"
                id="download_job-target_directory"
                name="target_directory"
                value={this.state.activeItem.target_directory}
                onChange={this.handleChange}
                placeholder="Download destination"
              />
            </FormGroup>
            <FormGroup>
              <Label for="download_job-target_file">Target file name</Label>
              <Input
                type="text"
                id="download_job-target_file"
                name="target_file"
                value={this.state.activeItem.target_file}
                onChange={this.handleChange}
                placeholder="File name"
              />
            </FormGroup>
          </Form>
        </ModalBody>
        <ModalFooter>
          <Button
            color="success"
            onClick={() => onSave(this.state.activeItem)}
          >
            Save
          </Button>
        </ModalFooter>
      </Modal>
    );
  }
}