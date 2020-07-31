#include "pugixml.hpp"

namespace plasma_source {

class XMLHelper {
    public:
        XMLHelper(const char* root_name);
        void set_root_element(const char* root_name);
        void add_element(const char* element_name, const char* element_value);
        void add_element(const char* element_name, double element_value);
        void add_element(const char* element_name, int element_value);
        void add_element(const char* element_name, std::string element_value);
        std::string to_string();
    
    private:
        pugi::xml_document doc;
        pugi::xml_node root_node;
};

}
