#include "pugixml.hpp"

namespace plasma_source {

class XMLHelper {
    public:
        XMLHelper(const char* root_name);
        XMLHelper(pugi::xml_document* doc, std::string root_name);
        void set_root_element(const char* root_name);
        void add_element(const char* element_name, const char* element_value);
        void add_element(const char* element_name, double element_value);
        void add_element(const char* element_name, int element_value);
        void add_element(const char* element_name, std::string element_value);
        double get_element_as_double(const char* element_name);
        int get_element_as_int(const char* element_name);
        std::string get_element_as_string(const char* element_name);
        std::string to_string();
    
    private:
        pugi::xml_document doc;
        pugi::xml_node root_node;
};

}
