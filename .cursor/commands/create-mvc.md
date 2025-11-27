# Create MVC Command

## Purpose

This command generates a complete MVC bundle for the given entity:

- Model (MVC model layer)
- Controller (MVC controller layer)
- Views (index/show/create/edit templates)
- Basic CRUD route hints

## Usage

```text
/create mvc <Entity>
```

### Examples

```text
/create mvc Car
/create mvc Listing
/create mvc User
```

## Behavior

This command delegates to:

- `create-mvc-model-agent`
- `create-mvc-controller-agent`
- `create-mvc-view-agent`

## Output

- Models saved to: `resolvePath(stack, "mvc.models")`
- Controllers saved to: `resolvePath(stack, "mvc.controllers")`
- Views saved to: `resolvePath(stack, "mvc.views")`
- Test files generated automatically (BDD & TDD)
