.. _secClassStructure:

Class structure
===============

AMPL API library consists of a collection of classes to interact with the underlying AMPL interpreter and to access
its inputs and outputs. It uses generic collections to represent the various entities which comprise a mathematical
model. The structure of these entities is explained in this section.  For a quick introduction to AMPL Entities see `Quick Introduction to AMPL <https://dev.ampl.com/ampl/introduction.html>`_.

The main class used to interact with AMPL, instantiate and interrogate the models is :class:`amplpy.AMPL`.
One object of this class represents an execution of an AMPL translator, and is the first class that has to be instantiated when
developing a solution based on AMPL API. It allows the interaction with the underlying AMPL translator, issuing commands,
getting diagnostics and controlling the process.

.. _secAMPLClass:

AMPL class
----------

For all calculations, AMPL API uses an underlying AMPL execution engine, which is wrapped by the class :class:`amplpy.AMPL`.
Thus, one instance of this class is the first object to be created when writing a program which uses the AMPL API
library. The object is quite resource-heavy, therefore it should be explicitly closed as soon as it is not needed anymore,
with a call to :func:`amplpy.AMPL.close()`.

All the model creation and structural alteration operations are to be expressed in AMPL language through the
AMPL main object; moreover, the class provides access to the current state represented via the classes derived
from :class:`amplpy.Entity`, as shown in section :ref:`secPythonAlgebraicEntitiesReference` and provides several other functionalities
(see :ref:`secReferencePython`).

The functions can be split in three groups: direct AMPL interaction, model interrogation and commands.

Method aliases: camelCase and snake_case
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Starting from version 0.8, we provide both camelCase (e.g., :func:`~amplpy.AMPL.readData`) and snake_case (e.g., :func:`~amplpy.AMPL.read_data`)
versions of methods for all our classes. Before version 0.8, only camelCase methods were available. The style guide
for Python Code `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_ recommends the use
of lowercase with words separated by underscores as necessary to improve readability for variables and method names.
However, in our APIs for other languages the predominant style is camelCase (e.g., R, C++, etc.) and in Python
snake_case is not always the style used. By providing aliases with both versions of the method names we give you
the freedom to choose the style you prefer.

Direct interaction with AMPL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The methods available to input AMPL commands are :func:`amplpy.AMPL.eval()`, :func:`amplpy.AMPL.read()` and :func:`amplpy.AMPL.read_data()`;
they send the strings specified (or the specified files) to the AMPL engine for interpretation.

Model interrogation
~~~~~~~~~~~~~~~~~~~

Evaluating AMPL files or statements creates various kind of entities in the underlying AMPL process.
To get the object (or, in general, programmatic) representation of such entities, the programmer can follow two main courses.

* Get an :class:`amplpy.EntityMap` of all available entities, to iterate through them. The methods to obtain such lists are:

  * :func:`amplpy.AMPL.get_variables()` gets the map of all the defined variables
  * :func:`amplpy.AMPL.get_constraints()` gets the map of all the defined constraints
  * :func:`amplpy.AMPL.get_objectives()` gets the map of all the defined objectives
  * :func:`amplpy.AMPL.get_sets()` gets the map of all the defined sets
  * :func:`amplpy.AMPL.get_parameters()` gets the map of all the defined parameters

* Knowing the AMPL name of an entity, use commands to get the specific entity directly:

  * :func:`amplpy.AMPL.get_variable()` returns the :class:`amplpy.Variable` representing the AMPL variable with the specified name, if it exists
  * :func:`amplpy.AMPL.get_constraint()` returns the :class:`amplpy.Constraint` representing the AMPL constraint with the specified name, if it exists
  * :func:`amplpy.AMPL.get_objective()` returns the :class:`amplpy.Objective` representing the AMPL objective with the specified name, if it exists
  * :func:`amplpy.AMPL.get_parameter()` returns the :class:`amplpy.Parameter` representing the AMPL parameter with the specified name, if it exists
  * :func:`amplpy.AMPL.get_set()` returns the :class:`amplpy.Set` representing the AMPL set with the specified name, if it exists


Once the desired entities have been created, it is possible to use their properties and methods to manipulate the model
and to extract or assign data. Updating the state of the programmatic entities is implemented lazily and uses proper
dependency handling. Communication with the underlying engine is therefore executed only when an entity's properties
are being accessed and only when necessary.
An entity is invalidated (needs refreshing) if one of the entities it depends from has been manipulated or if a generic
AMPL statement evaluation is performed (through :func:`amplpy.AMPL.eval()` or similar routines). This is one of the reasons
why it is generally better to use the embedded functionalities (e.g. fixing a variable through the corresponding API
function call) than using AMPL statements: in the latter case, the API invalidates all entities, as the effects of
such generic statements cannot be predicted.
Refreshing is transparent to the user, but must be taken into account when implementing functions
which access data or modify entities frequently.

.. _secAlternativeMethodToAccessEntities:

Alternative method to access entities
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For those that prefer a less verbose syntax,
there is an alternative and more compact syntax for accessing entities and options:

* Accessing ``ampl.var[name]`` is equivalent to ``ampl.get_variable(name)`` (:func:`~amplpy.AMPL.get_variable`);
* Accessing ``ampl.con[name]`` is equivalent to ``ampl.get_constraint(name)`` (:func:`~amplpy.AMPL.get_constraint`);
* Accessing ``ampl.obj[name]`` is equivalent to ``ampl.get_objective(name)`` (:func:`~amplpy.AMPL.get_objective`);
* Accessing ``ampl.set[name]`` is equivalent to ``ampl.get_set(name)`` (:func:`~amplpy.AMPL.get_set`);
* Accessing ``ampl.param[name]`` is equivalent to ``ampl.get_parameter(name)`` (:func:`~amplpy.AMPL.get_parameter`);
* Accessing ``ampl.option[name]`` is equivalent to ``ampl.get_option(name)`` (:func:`~amplpy.AMPL.get_option`).

Setting entities and options is also possible:

* ``ampl.var[name] = value`` is equivalent to ``ampl.get_variable(name).set_value(value)``  (:func:`~amplpy.Variable.set_value`);
* ``ampl.con[name] = value`` is equivalent to ``ampl.get_constraint(name).set_dual(value)`` (:func:`~amplpy.Constraint.set_dual`);
* ``ampl.set[name] = values`` is equivalent to ``ampl.get_set(name).set_values(values)`` (:func:`~amplpy.Set.set_values`);
* ``ampl.param[name] = value`` is equivalent to ``ampl.get_parameter(name).set(value)`` if the parameter is scalar (:func:`~amplpy.Parameter.set`), ``ampl.get_parameter(name).set_values(value)`` otherwise (:func:`~amplpy.Parameter.set_values`);
* ``ampl.option[name] = value`` is equivalent to ``ampl.set_option(name, value)`` (:func:`~amplpy.AMPL.set_option`).


Commands and options
~~~~~~~~~~~~~~~~~~~~

Some AMPL commands are encapsulated by functions in the :class:`amplpy.AMPL` class for ease of access.
These comprise :func:`amplpy.AMPL.solve()` and others.
To access and set options in AMPL, the functions :func:`amplpy.AMPL.get_option()`
and :func:`amplpy.AMPL.set_option()` are provided.
These functions provide an easier programmatic access to the AMPL options.
In general, when an encapsulation is available for an AMPL command, the programmatic access to it is to be preferred to calling the same command using
:func:`amplpy.AMPL.eval()`.


Output and errors handling
~~~~~~~~~~~~~~~~~~~~~~~~~~

The output from the AMPL translator is handled implementing the interface :class:`amplpy.OutputHandler`.
The method :func:`amplpy.OutputHandler.output()` is called at each block of output from the translator. The current output handler
can be accessed and set via :func:`amplpy.AMPL.get_output_handler()`
and :func:`amplpy.AMPL.set_output_handler()`;
the default output handler prints each block to the standard console output.

Error handling is two-faced:

* Errors coming from the underlying AMPL translator (e.g. syntax errors and warnings obtained calling the :func:`amplpy.AMPL.eval()` method)
  are handled by the :class:`amplpy.ErrorHandler` which can be set and get via :func:`amplpy.AMPL.get_error_handler()`
  and :func:`amplpy.AMPL.set_error_handler()`.
* Generic errors coming from the API, which are detected outside the translator are thrown as exceptions.

The default implementation of the error handler throws exceptions on errors and prints the warnings to stdout.



.. _secModellingClasses:

Modelling entities classes
--------------------------

This group of classes represents the basic entities of an AMPL optimisation
model: variables, constraints, objectives, parameters and sets.
They are used to access the current state of the AMPL translator
(e.g. to find the values of a variable), and to some extent they can be
used for data input (e.g. assign values to a parameter, fix a variable).

Objects of these classes cannot be created programmatically by the user: the model creation and structural
modification is handled in AMPL (see section :ref:`secAMPLClass`), through the methods :func:`amplpy.AMPL.eval()`
and :func:`amplpy.AMPL.read()`. The base class is :class:`amplpy.Entity`.

The classes derived from :class:`amplpy.Entity` represent algebraic entites
(e.g. a variable indexed over a set in AMPL), and are implemented as a map
from an object (number, string or tuple) to an instance which allow access
to its instances (methods :func:`amplpy.Entity.__getitem__` and
:func:`amplpy.Entity.get()`).
The case of scalar entities (like the AMPL entity defined by ``var x;``) is handled at Entity level, and will be
illustrated in the paragraph regarding instances below.
The derived classes are: :class:`amplpy.Variable`, :class:`amplpy.Constraint`, :class:`amplpy.Parameter`,
:class:`amplpy.Objective` and :class:`amplpy.Set`.

Any instance object represents a single instance of an algebraic entity
(e.g.  the value of a variable for a specific value of its indexing set),
and is treated as a scalar entity.
Entities and instances are both handled by the class :class:`amplpy.Entity`.
An entity (algebraic entity in AMPL)
can contain various instance objects (instances in AMPL), while each instance has to be part of exactly one
entity. The exact methods and properties of the entity depend on the particular kind of entity under consideration
(i.e. variable, constraint, parameter).

As an example, for indexed entities, the class :class:`amplpy.Variable` has functionalities like :func:`amplpy.Variable.fix()` and :func:`amplpy.Variable.unfix()`,
which would fix or unfix all instances which are part of the algebraic entity, and for instances the
class :class:`amplpy.Variable` has properties like :func:`amplpy.Variable.value()`
and :func:`amplpy.Variable.dual()` (together with instance level fix and unfix methods).

The class :class:`amplpy.Constraint` has functionalities like :func:`amplpy.Constraint.drop()` and
:func:`amplpy.Constraint.restore()` on its entity level,
and on its instance level it has properties like :func:`amplpy.Constraint.body()` and
:func:`amplpy.Constraint.dual()`
(and methods like drop and restore for the single instance).

Note that the class :class:`amplpy.Parameter`, which represent an algebraic parameter, represents
its instances by objects (typically double numbers or strings) and therefore does not have special methods
on its instance level.


.. _secAccessInstancesAndValues:

Access to instances and values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The instances can be accessed from the parent entity through functions like :func:`amplpy.Entity.get()`, available for
all entity classes or via the indexing operator.
All data corresponding to the entity can be accessed through the instances, but the computational overhead of such kind of
access is quite considerable. To avoid this, the user can gain bulk data access through a :class:`amplpy.DataFrame` object;
reference to these object can be obtained using :func:`amplpy.Entity.get_values` methods.
In case of scalar entities (e.g. the entity declared in AMPL with the statement ``var x;``), all the instance specific methods are
replicated at Entity level, to allow the code fragment ``value = x.value()`` instead of the more explicit ``value = x.get().value()``.
See example below:


.. code-block:: python

   from amplpy import AMPL
   ampl = AMPL()
   ampl.eval('var x;')
   x = ampl.get_variable('x')
   value = x.value()        # Compact access to scalar entities
   value = x.get().value()  # Access through explicit reference to the instance


Indexed entities are central in modelling via AMPL. This is why the :func:`amplpy.Entity.get()` method
and the indexing operator can be used in multiple ways, to adapt to specific use cases.
These will be presented below, by mean of some examples.



**Scalar Entities** In general, as seen above, access to an instance of a scalar entity is not needed, as all functionalities of the instance are replicated at entity level in this case. Anyway,
to gain explicit access to an instance, the function :func:`amplpy.Entity.get()` can be used without parameters, as shown below.

.. code-block:: python

   ampl.eval('var x;')
   x = ampl.get_variable('x').get()

**Indexed Entities** Instances of indexed entities can be accessed as shown below:

.. code-block:: python

   from amplpy import AMPL
   ampl = AMPL()
   ampl.eval('var x{1..2, 4..5, 7..8};')
   x = ampl.get_variable('x')

   # Option 1:
   instance = x[1, 4, 7]
   # Option 2:
   instance = x.get(1, 4, 7)

   index = (1, 4, 7)
   # Option 3:
   instance = x[index]
   # Option 4:
   instance = x.get(index)


AMPL API allows access to the instances through iterators. See the examples below which use
the same declarations of the example above to illustrate how to:

* Find if an instance exists or not
* Enumerate all the instances

.. code-block:: python

  # Find using iterator
  instance = x.find(t)
  if instance is None:
      print("Instance not found")

  # Access all instances using an iterator
  for index, instance in x:
      print(index, instance.name())

  # Create a dictionary mapping each index to the corresponding instance
  xdict = dict(x)


The currently defined entities are obtained from the various get methods of the :class:`amplpy.AMPL` object
(see section :ref:`secAMPLClass`). Once a reference to an entity is created, the entity is automatically kept up-to-date
with the corresponding entity in the AMPL interpreter. That is, if a reference to a newly created AMPL variable
is obtained by means of :func:`amplpy.AMPL.get_variable()`, and the model the variable is part of is then solved
by means of :func:`amplpy.AMPL.solve()`, the values of the instances of the variable will automatically be updated.
The following code snippet should demonstrate the concept.

.. code-block:: python

   ampl.eval('var x;')
   ampl.eval('maximize z: x;')
   ampl.eval('subject to c: x<=10;')
   x = ampl.get_variable('x')

   # At this point x.value() evaluates to 0
   print(x.value())  # prints 0

   ampl.solve()

   # At this point x.value() evaluates to 10
   print(x.value())  # prints 10


Relation between entities and data
----------------------------------

The entities and instances in AMPL store data (numbers or strings) and can be indexed, hence the instances available depend
on the values in the indexing set(s).  The order in which these indexing sets is handled in the AMPL entities is
not always consistent with the ordering in which the data for such sets is defined, so it is often desirable, even when interested
in only data (decoupled from the AMPL entities) to keep track of the indexing values which corresponds to each value.

Moreover, when dealing with AMPL entities (like :class:`amplpy.Variable`), consistency is guaranteed for every instance.
This means that, if a reference to an instance is kept and in the underlying AMPL interpreter the value of the instance
is changed, the value read from the instance object will be always consistent with the AMPL value and, if an instance is
deleted in AMPL, an exception will be thrown when accessing it. This has the obvious benefit of allowing the user to rely
on the values of the instances, but has a price in terms of computational overhead. For example, accessing in this way the value
of 1000 instances:

.. code-block:: python

  from amplpy import AMPL
  ampl = AMPL()
  ampl.eval('set A := 1..1000; param c{i in A} default 0; var x{i in 1..1000} := c[i];')

  # Enumerate through all the instances of c and set their values
  c = ampl.get_parameter("c");
  for i in range(1, c.num_instances()+1):
      c[i] = i*1.1

  # Enumerate through all the instances and print their values
  x = ampl.get_variable("x")
  for index, xi in x:
      print(xi.value())


will check at each access if the referenced instance is valid or not, resulting in a computational overhead.

To ease data communication and handling, the class :class:`amplpy.DataFrame` is provided. Its usage is two-fold:

* It allows definition of data for multiple parameters in one single call to the underlying interpterer
* It decouples data and entities, reducing the computational overhead and risks related to concurrency

`amplpy.DataFrame` objects should therefore be used in these circumnstances, together with the methods
:func:`amplpy.AMPL.set_data()` and :func:`amplpy.Entity.get_values()`.

.. code-block:: python

  # Create a new dataframe with one indexing column (A) and another column (c)
  from amplpy import AMPL, DataFrame
  df = DataFrame(index='A', columns='c')
  for i in range(1, 1000+1):
      df.add_row(i, i*1.1)

  ampl = AMPL()
  ampl.eval('set A; param c{i in A} default 0; var x{i in A} := c[i];')
  # Assign data to the set A and the parameter c in one line
  ampl.set_data(df, 'A')

  x = ampl.get_variable('x')
  # From the following line onwards, df is uncoupled from the
  # modelling system,
  df = x.get_values()

  # Prints all the values
  for row in df:
      print(row)

  # Retrieve all rows
  rows = [tuple(row) for row in df]

  # Prints all the values in the DataFrame
  print(df)


The underlying AMPL interpreter does not need to be open when using the dataframe object, but it maintains all
the correspondence between indexing set and actual value of the instances.


.. _secAccessToScalars:

Access to scalar values
~~~~~~~~~~~~~~~~~~~~~~~

Simplified access to scalar values, like the value of a scalar variable or parameter or, in general, any
AMPL expression that can be evaluated to a single string or number, is possible using the convenience method :func:`amplpy.AMPL.get_value()`.
This method will fail if called on an AMPL expression which does not evaluate to a single value. See below for an example:


.. code-block:: python

  from amplpy import AMPL
  ampl = AMPL()
  ampl.eval('var x{i in 1..3} := i;')
  ampl.eval('param p symbolic := "test";')
  ampl.eval('param pp := 4;')
  # x2 will have the value 2
  print(ampl.get_value("x[2]"))
  # p will have the value "test"
  print(ampl.get_value('p'))
  # pp will have the value 4
  print(ampl.get_value('pp'))


