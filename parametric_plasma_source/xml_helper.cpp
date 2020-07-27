#include <sstream>
#include <iostream>
#include "xml_helper.hpp"
#include "pugixml.hpp"

namespace plasma_source {

  XMLHelper::XMLHelper(const char* root_name) {
    root_node = doc.append_child(root_name);
  }

  XMLHelper::XMLHelper(pugi::xml_document* doc, std::string root_name) {
    this->doc.reset(*doc);
    this->root_node = this->doc.root().child(root_name.c_str());
  }

  void XMLHelper::set_root_element(const char* root_name) {
    root_node = doc.append_child(root_name);
  }

  void XMLHelper::add_element(const char* element_name, const char* element_value) {
    root_node.append_child(element_name).text() = element_value;
  }

  void XMLHelper::add_element(const char* element_name, double element_value) {
    root_node.append_child(element_name).text() = element_value;
  }

  void XMLHelper::add_element(const char* element_name, int32_t element_value) {
    root_node.append_child(element_name).text() = element_value;
  }

  void XMLHelper::add_element(const char* element_name, std::string element_value) {
    root_node.append_child(element_name).text() = element_value.c_str();
  }

  double XMLHelper::get_element_as_double(const char* element_name) {
    return root_node.child(element_name).text().as_double();
  }

  int XMLHelper::get_element_as_int(const char* element_name) {
    return root_node.child(element_name).text().as_int();
  }

  std::string XMLHelper::get_element_as_string(const char* element_name) {
    return root_node.child(element_name).text().as_string();
  }

  struct xml_string_writer: pugi::xml_writer {
    std::string result;

    virtual void write(const void* data, size_t size) {
      result.append(static_cast<const char*>(data), size);
    }
  };

  std::string XMLHelper::to_string() {
    xml_string_writer writer;
    doc.print(writer, "  ");

    return writer.result;
  }

}