from selenium.webdriver.remote.webelement import WebElement

from ..utilities.utilities import Utilities
import os
import shutil


class ElementContext(object):
    def __init__(self, ctx):
        self.ctx = ctx

    @property
    def driver(self):
        return self.ctx.driver

    @property
    def element_finder(self):
        return self.ctx._element_finder

    @element_finder.setter
    def element_finder(self, value):
        self.ctx._element_finder = value

    @property
    def event_firing_webdriver(self):
        return self.ctx.event_firing_webdriver

    @event_firing_webdriver.setter
    def event_firing_webdriver(self, event_firing_webdriver):
        self.ctx.event_firing_webdriver = event_firing_webdriver

    def find_element(self, locator, tag=None, required=True, parent=None):
        """Find element matching `locator`.

        :param locator: Locator to use when searching the element.
            See library documentation for the supported locator syntax.
        :type locator: str or selenium.webdriver.remote.webelement.WebElement
        :param tag: Limit searching only to these elements.
        :type tag: str
        :param required: Raise `ElementNotFound` if element not found when
            true, return `None` otherwise.
        :type required: True or False
        :param parent: Optional parent `WebElememt` to search child elements
            from. By default, search starts from the root using `WebDriver`.
        :type parent: selenium.webdriver.remote.webelement.WebElement
        :return: Found `WebElement` or `None` if element not found and
            `required` is false.
        :rtype: selenium.webdriver.remote.webelement.WebElement
        :raises SeleniumLibrary.errors.ElementNotFound: If element not found
            and `required` is true.
        """
        return self.element_finder.find(locator, tag, True, required, parent)

    def find_elements(self, locator, tag=None, parent=None):
        """Find all elements matching `locator`.

        :param locator: Locator to use when searching the element.
            See library documentation for the supported locator syntax.
        :type locator: str or selenium.webdriver.remote.webelement.WebElement
        :param tag: Limit searching only to these elements.
        :type tag: str
        :param parent: Optional parent `WebElememt` to search child elements
            from. By default, search starts from the root using `WebDriver`.
        :type parent: selenium.webdriver.remote.webelement.WebElement
        :return: list of found `WebElement` or empty if elements are not found.
        :rtype: list[selenium.webdriver.remote.webelement.WebElement]
        """
        return self.element_finder.find(locator, tag, False, False, parent)


class FindElement(ElementContext):
    def __init__(self, ctx):
        ElementContext.__init__(self, ctx)

        self._strategies = {
            'id': self._find_by_id,
            'name': self._find_by_name,
            'xpath': self._find_by_xpath,
            'dom': self._find_by_dom,
            'link': self._find_by_link_text,
            'partial-link': self._find_by_partial_link_text,
            'css': self._find_by_css_selector,
            'class': self._find_by_class_name,
            'tag': self._find_by_tag_name,
            'href': self._find_element_by_href,
        }

        self._key_attrs = {
            None: ['@id', '@name'],
            'a': ['@id', '@name', '@href',
                  'normalize-space(descendant-or-self::text())'],
            'img': ['@id', '@name', '@src', '@alt'],
            'input': ['@id', '@name', '@value', '@src'],
            'button': ['@id', '@name', '@value',
                       'normalize-space(descendant-or-self::text())']
        }

    def _get_tag_and_constraints(self, tag):
        if tag is None:
            return None, {}
        tag = tag.lower()
        constraints = {}
        if tag == 'link':
            tag = 'a'
        if tag == 'partial-link':
            tag = 'a'
        elif tag == 'image':
            tag = 'img'
        elif tag == 'list':
            tag = 'select'
        elif tag == 'radio button':
            tag = 'input'
            constraints['type'] = 'radio'
        elif tag == 'checkbox':
            tag = 'input'
            constraints['type'] = 'checkbox'
        elif tag == 'text field':
            tag = 'input'
            constraints['type'] = ['date', 'datetime-local', 'email', 'month',
                                   'number', 'password', 'search', 'tel',
                                   'text', 'time', 'url', 'week', 'file']
        elif tag == 'file upload':
            tag = 'input'
            constraints['type'] = 'file'
        elif tag == 'text area':
            tag = 'textarea'
        return tag, constraints

    def _parse_locator(self, locator):
        r_locator = locator.split('=')
        if len(r_locator) > 1:
            return r_locator[0], r_locator[1]
        else:
            raise AssertionError('Invalid locator %s' % locator)

    def _is_webelement(self, locator):
        return isinstance(locator, WebElement)

    def find_element(self, locator, tag=None, first_only=True, required=True, parent=None):
        return self.find(locator, tag, True, required, parent)

    def find_elements(self, locator, tag=None, parent=None):
        return self.find(locator, tag, False, False, parent)

    def find(self, locator, tag=None, first_only=True, required=True,
             parent=None):
        element_type = 'Element' if not tag else tag.capitalize()
        if parent and not self._is_webelement(parent):
            raise ValueError('Parent must be Selenium WebElement but it '
                             'was {}.'.format(type(parent)))
        if self._is_webelement(locator):
            return locator
        prefix, criteria = self._parse_locator(locator)
        strategy = self._strategies[prefix]
        tag, constraints = self._get_tag_and_constraints(tag)
        elements = strategy(criteria, tag, constraints,
                            parent=parent or self.driver)
        if required and not elements:
            raise AssertionError("%s with locator '%s' not found." % (element_type, locator))
        if first_only:
            if not elements:
                return None
            return elements[0]
        return elements

    def _filter_element(self, elements, tag, constraints):
        _filtered_list = []
        for e in elements:
            if tag is not None and e.tag_name == tag.lower():
                _filtered_list.append(e)
            for c in constraints:
                if isinstance(constraints[c], list):
                    if e.get_attribute(c) in constraints[c]:
                        _filtered_list.append(e)
                        break
                elif e.get_attribute(c) == constraints[c]:
                    _filtered_list.append(e)
                    break
        return elements if len(_filtered_list) == 0 else _filtered_list

    def _find_by_id(self, criteria, tag, constraints, parent):
        elements = parent.find_elements_by_id(criteria)
        return self._filter_element(elements, tag, constraints)

    def _find_by_name(self, criteria, tag, constraints, parent):
        elements = parent.find_elements_by_name(criteria)
        return self._filter_element(elements, tag, constraints)

    def _find_by_xpath(self, criteria, tag, constraints, parent):
        elements = parent.find_elements_by_xpath(criteria)
        return self._filter_element(elements, tag, constraints)

    def _find_by_dom(self, criteria, tag, constraints, parent):
        if self._is_webelement(parent):
            raise ValueError('This method does not allow WebElement as parent')
        result = self.driver.execute_script("return %s;" % criteria)
        if result is None:
            return []
        if not isinstance(result, list):
            result = [result]
        return self._filter_element(result, tag, constraints)

    def _find_by_css_selector(self, criteria, tag, constraints, parent):
        elements = parent.find_elements_by_css_selector(criteria)
        return self._filter_element(elements, tag, constraints)

    def _find_by_class_name(self, criteria, tag, constraints, parent):
        elements = parent.find_elements_by_class_name(criteria)
        return self._filter_element(elements, tag, constraints)

    def _find_by_tag_name(self, criteria, tag, constraints, parent):
        elements = parent.find_elements_by_tag_name(criteria)
        return self._filter_element(elements, tag, constraints)

    def _find_by_link_text(self, criteria, tag, constraints, parent):
        elements = parent.find_elements_by_link_text(criteria)
        return self._filter_element(elements, tag, constraints)

    def _find_by_partial_link_text(self, criteria, tag, constraints, parent):
        elements = parent.find_elements_by_partial_link_text(criteria)
        return self._filter_element(elements, tag, constraints)

    def _find_element_by_href(self, criteria, tag, constraints=None, parent=None):
        elements = parent.find_elements_by_css_selector("*[href='"+criteria+"']")
        return self._filter_element(elements, 'a', constraints)



