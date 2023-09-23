# aldebaran_cms
Databaseless CMS structured and interpreted by Markdown-files in folders

### Date: 2023-09-23

## Development progress

1. **Code Organization and Modularization**
   - [ ] Refactor code into smaller functions to enhance readability and maintainability.
   - [ ] Group related functionalities into modules or services to promote separation of concerns.

2. **Error Handling**
   - [ ] Implement detailed error handling for various edge cases, especially for file reading and routing.
   - [ ] Ensure that all raised exceptions have meaningful messages for easier debugging.

3. **Optimization**
   - [ ] Investigate caching strategies to reduce redundant reads from the filesystem.
   - [ ] Reevaluate the use of `lru_cache` to see if it's being used effectively.

4. **Documentation**
   - [ ] Document functions, routes, and modules with meaningful docstrings.
   - [ ] Create a detailed README that explains the purpose, setup process, and usage of your CMS.

5. **Tests**
   - [ ] Write unit tests for functions and integration tests for routes.
   - [ ] Implement mock tests for file operations to ensure tests don't rely on specific file content.

6. **Security**
   - [ ] Ensure that user inputs are being sanitized and validated to prevent potential security threats.
   - [ ] Check for potential vulnerabilities in how you're processing and rendering markdown.

7. **Template Refinements**
   - [ ] Ensure that the Jinja templates are not relying on hardcoded values. Parameterize where necessary.
   - [ ] Optimize the styles and scripts being loaded for better page load performance.

8. **Responsive Design**
   - [ ] Check the responsiveness of your CMS on different devices and screen sizes.
   - [ ] Refine CSS and HTML to ensure a consistent experience across platforms.

9. **Code Quality**
   - [ ] Run a code linter (e.g., `flake8` or `black`) to ensure that the code follows PEP 8 standards.
   - [ ] type hints throughout the codebase for better type safety.

10. **Extensions and Features**
   - [ ] Consider implementing a search functionality for content.
   - [ ] Think about how users might extend the CMS or add plugins.
