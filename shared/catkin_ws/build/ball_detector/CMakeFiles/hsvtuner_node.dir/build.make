# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.10

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/shared/catkin_ws/src

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/shared/catkin_ws/build

# Include any dependencies generated for this target.
include ball_detector/CMakeFiles/hsvtuner_node.dir/depend.make

# Include the progress variables for this target.
include ball_detector/CMakeFiles/hsvtuner_node.dir/progress.make

# Include the compile flags for this target's objects.
include ball_detector/CMakeFiles/hsvtuner_node.dir/flags.make

ball_detector/CMakeFiles/hsvtuner_node.dir/src/hsvTuner.cpp.o: ball_detector/CMakeFiles/hsvtuner_node.dir/flags.make
ball_detector/CMakeFiles/hsvtuner_node.dir/src/hsvTuner.cpp.o: /home/shared/catkin_ws/src/ball_detector/src/hsvTuner.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/shared/catkin_ws/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object ball_detector/CMakeFiles/hsvtuner_node.dir/src/hsvTuner.cpp.o"
	cd /home/shared/catkin_ws/build/ball_detector && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/hsvtuner_node.dir/src/hsvTuner.cpp.o -c /home/shared/catkin_ws/src/ball_detector/src/hsvTuner.cpp

ball_detector/CMakeFiles/hsvtuner_node.dir/src/hsvTuner.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/hsvtuner_node.dir/src/hsvTuner.cpp.i"
	cd /home/shared/catkin_ws/build/ball_detector && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/shared/catkin_ws/src/ball_detector/src/hsvTuner.cpp > CMakeFiles/hsvtuner_node.dir/src/hsvTuner.cpp.i

ball_detector/CMakeFiles/hsvtuner_node.dir/src/hsvTuner.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/hsvtuner_node.dir/src/hsvTuner.cpp.s"
	cd /home/shared/catkin_ws/build/ball_detector && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/shared/catkin_ws/src/ball_detector/src/hsvTuner.cpp -o CMakeFiles/hsvtuner_node.dir/src/hsvTuner.cpp.s

ball_detector/CMakeFiles/hsvtuner_node.dir/src/hsvTuner.cpp.o.requires:

.PHONY : ball_detector/CMakeFiles/hsvtuner_node.dir/src/hsvTuner.cpp.o.requires

ball_detector/CMakeFiles/hsvtuner_node.dir/src/hsvTuner.cpp.o.provides: ball_detector/CMakeFiles/hsvtuner_node.dir/src/hsvTuner.cpp.o.requires
	$(MAKE) -f ball_detector/CMakeFiles/hsvtuner_node.dir/build.make ball_detector/CMakeFiles/hsvtuner_node.dir/src/hsvTuner.cpp.o.provides.build
.PHONY : ball_detector/CMakeFiles/hsvtuner_node.dir/src/hsvTuner.cpp.o.provides

ball_detector/CMakeFiles/hsvtuner_node.dir/src/hsvTuner.cpp.o.provides.build: ball_detector/CMakeFiles/hsvtuner_node.dir/src/hsvTuner.cpp.o


# Object files for target hsvtuner_node
hsvtuner_node_OBJECTS = \
"CMakeFiles/hsvtuner_node.dir/src/hsvTuner.cpp.o"

# External object files for target hsvtuner_node
hsvtuner_node_EXTERNAL_OBJECTS =

/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: ball_detector/CMakeFiles/hsvtuner_node.dir/src/hsvTuner.cpp.o
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: ball_detector/CMakeFiles/hsvtuner_node.dir/build.make
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_shape.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_stitching.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_superres.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_videostab.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_aruco.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_bgsegm.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_bioinspired.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_ccalib.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_datasets.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_dpm.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_face.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_freetype.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_fuzzy.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_hdf.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_line_descriptor.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_optflow.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_plot.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_reg.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_saliency.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_stereo.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_structured_light.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_surface_matching.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_text.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_ximgproc.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_xobjdetect.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_xphoto.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /opt/ros/melodic/lib/libcv_bridge.so
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_core.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_imgproc.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_imgcodecs.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /opt/ros/melodic/lib/libimage_transport.so
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /opt/ros/melodic/lib/libmessage_filters.so
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /opt/ros/melodic/lib/libclass_loader.so
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/libPocoFoundation.so
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libdl.so
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /opt/ros/melodic/lib/libroscpp.so
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /opt/ros/melodic/lib/librosconsole.so
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /opt/ros/melodic/lib/librosconsole_log4cxx.so
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /opt/ros/melodic/lib/librosconsole_backend_interface.so
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/liblog4cxx.so
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libboost_regex.so
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /opt/ros/melodic/lib/libxmlrpcpp.so
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /opt/ros/melodic/lib/libroslib.so
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /opt/ros/melodic/lib/librospack.so
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libpython2.7.so
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libboost_filesystem.so
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libboost_program_options.so
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libtinyxml2.so
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /opt/ros/melodic/lib/libroscpp_serialization.so
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /opt/ros/melodic/lib/librostime.so
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /opt/ros/melodic/lib/libcpp_common.so
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libboost_system.so
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libboost_thread.so
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libboost_chrono.so
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libboost_date_time.so
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libboost_atomic.so
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libpthread.so
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libconsole_bridge.so.0.4
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_video.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_viz.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_phase_unwrapping.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_rgbd.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_calib3d.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_features2d.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_flann.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_objdetect.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_ml.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_highgui.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_photo.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_videoio.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_imgcodecs.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_imgproc.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: /usr/lib/aarch64-linux-gnu/libopencv_core.so.3.2.0
/home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node: ball_detector/CMakeFiles/hsvtuner_node.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/shared/catkin_ws/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable /home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node"
	cd /home/shared/catkin_ws/build/ball_detector && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/hsvtuner_node.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
ball_detector/CMakeFiles/hsvtuner_node.dir/build: /home/shared/catkin_ws/devel/lib/ball_detector/hsvtuner_node

.PHONY : ball_detector/CMakeFiles/hsvtuner_node.dir/build

ball_detector/CMakeFiles/hsvtuner_node.dir/requires: ball_detector/CMakeFiles/hsvtuner_node.dir/src/hsvTuner.cpp.o.requires

.PHONY : ball_detector/CMakeFiles/hsvtuner_node.dir/requires

ball_detector/CMakeFiles/hsvtuner_node.dir/clean:
	cd /home/shared/catkin_ws/build/ball_detector && $(CMAKE_COMMAND) -P CMakeFiles/hsvtuner_node.dir/cmake_clean.cmake
.PHONY : ball_detector/CMakeFiles/hsvtuner_node.dir/clean

ball_detector/CMakeFiles/hsvtuner_node.dir/depend:
	cd /home/shared/catkin_ws/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/shared/catkin_ws/src /home/shared/catkin_ws/src/ball_detector /home/shared/catkin_ws/build /home/shared/catkin_ws/build/ball_detector /home/shared/catkin_ws/build/ball_detector/CMakeFiles/hsvtuner_node.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : ball_detector/CMakeFiles/hsvtuner_node.dir/depend

